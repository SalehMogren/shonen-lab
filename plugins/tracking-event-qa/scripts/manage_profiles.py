#!/usr/bin/env python3
"""Manage non-secret tracking-event QA profiles."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = Path.home() / ".config" / "tracking-event-qa" / "profiles.json"
PROFILE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DEFAULT_PLATFORM_VALUES = {
    "web": ["web"],
    "app": ["posthog-react-native"],
    "backend": ["posthog-node", "posthog-python", "posthog-php", "posthog-go"],
}
SUPPORTED_PLATFORMS = frozenset(DEFAULT_PLATFORM_VALUES)


def load_store(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "active_profile": None, "profiles": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Could not read profile store {path}: {exc}") from exc
    validate_store(data)
    return data


def validate_store(data: Any) -> None:
    if not isinstance(data, dict) or data.get("version") != 1:
        raise SystemExit("Profile store must be a version 1 JSON object.")
    profiles = data.get("profiles")
    if not isinstance(profiles, dict):
        raise SystemExit("Profile store is missing the profiles object.")
    active = data.get("active_profile")
    if active is not None and active not in profiles:
        raise SystemExit(f"Active profile {active!r} does not exist.")
    for name, profile in profiles.items():
        validate_profile(name, profile)


def validate_profile(name: str, profile: Any) -> None:
    if not PROFILE_RE.fullmatch(name):
        raise SystemExit(f"Invalid profile name {name!r}; use lowercase hyphen-case.")
    if not isinstance(profile, dict):
        raise SystemExit(f"Profile {name!r} must be an object.")
    for key in ("squad", "product", "notion", "posthog"):
        if not profile.get(key):
            raise SystemExit(f"Profile {name!r} is missing {key!r}.")
    notion = profile["notion"]
    posthog = profile["posthog"]
    if not isinstance(notion, dict) or not notion.get("source"):
        raise SystemExit(f"Profile {name!r} needs notion.source.")
    if not isinstance(posthog, dict) or not posthog.get("project_id"):
        raise SystemExit(f"Profile {name!r} needs posthog.project_id.")
    if not posthog.get("platform_property"):
        raise SystemExit(f"Profile {name!r} needs posthog.platform_property.")
    validate_platform_values(name, posthog.get("platform_values"))
    thresholds = posthog.get("thresholds", {})
    for field in ("lookback_days", "recency_days", "live_volume"):
        if int(thresholds.get(field, 0)) <= 0:
            raise SystemExit(f"Profile {name!r} needs a positive posthog.thresholds.{field}.")
    if int(thresholds["recency_days"]) > int(thresholds["lookback_days"]):
        raise SystemExit(f"Profile {name!r} needs recency_days <= lookback_days.")


def validate_platform_values(name: str, value: Any) -> None:
    if not isinstance(value, dict) or not value:
        raise SystemExit(f"Profile {name!r} needs a non-empty posthog.platform_values object.")
    mapped_values = 0
    for platform, values in value.items():
        if not isinstance(platform, str) or not platform.strip():
            raise SystemExit(f"Profile {name!r} has an invalid platform name.")
        if platform not in SUPPORTED_PLATFORMS:
            supported = ", ".join(sorted(SUPPORTED_PLATFORMS))
            raise SystemExit(f"Profile {name!r} platform {platform!r} is unsupported; use {supported}.")
        if not isinstance(values, list):
            raise SystemExit(f"Profile {name!r} platform {platform!r} must map to a list.")
        if any(not isinstance(item, str) or not item.strip() for item in values):
            raise SystemExit(f"Profile {name!r} platform {platform!r} has an invalid value.")
        if len(values) != len(set(values)):
            raise SystemExit(f"Profile {name!r} platform {platform!r} has duplicate values.")
        mapped_values += len(values)
    if mapped_values == 0:
        raise SystemExit(f"Profile {name!r} needs at least one mapped platform value.")


def parse_platform_values(value: str) -> dict[str, list[str]]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"platform values must be valid JSON: {exc.msg}") from exc
    try:
        validate_platform_values("candidate", parsed)
    except SystemExit as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc
    return parsed


def atomic_write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix="profiles-", suffix=".json", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
        os.chmod(temp_path, 0o600)
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def profile_from_args(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "squad": args.squad,
        "product": args.product,
        "notion": {
            "source": args.notion_source,
            "event_name_property": args.event_name_property,
            "app_status_property": args.app_status_property,
            "web_status_property": args.web_status_property,
            "tracking_platform_property": args.tracking_platform_property,
            "assignee_property": args.assignee_property,
            "last_verified_property": args.last_verified_property,
            "verification_note_property": args.verification_note_property,
            "reproduce_link_property": args.reproduce_link_property,
            "qa_value": args.qa_value,
            "live_value": args.live_value,
        },
        "posthog": {
            "project_name": args.posthog_project_name,
            "project_id": str(args.posthog_project_id),
            "platform_property": args.platform_property,
            "platform_values": args.platform_values_json
            or {key: list(values) for key, values in DEFAULT_PLATFORM_VALUES.items()},
            "thresholds": {
                "lookback_days": args.lookback_days,
                "recency_days": args.recency_days,
                "live_volume": args.live_volume,
            },
        },
        "jira": {
            "project_key": args.jira_project_key,
            "issue_type": args.jira_issue_type,
        },
    }


def command_save(args: argparse.Namespace) -> None:
    store = load_store(args.config_path)
    if args.name in store["profiles"] and not args.replace:
        raise SystemExit(f"Profile {args.name!r} already exists; pass --replace to update it.")
    profile = profile_from_args(args)
    validate_profile(args.name, profile)
    store["profiles"][args.name] = profile
    if args.activate or store["active_profile"] is None:
        store["active_profile"] = args.name
    atomic_write(args.config_path, store)
    print(json.dumps({"saved": args.name, "active_profile": store["active_profile"], "path": str(args.config_path)}))


def command_list(args: argparse.Namespace) -> None:
    store = load_store(args.config_path)
    if args.json:
        print(json.dumps(store, indent=2, ensure_ascii=False, sort_keys=True))
        return
    print(f"Profile store: {args.config_path}")
    if not store["profiles"]:
        print("No profiles configured.")
        return
    for name, profile in sorted(store["profiles"].items()):
        marker = "*" if name == store["active_profile"] else " "
        print(f"{marker} {name}: {profile['squad']} / {profile['product']}")


def command_show(args: argparse.Namespace) -> None:
    store = load_store(args.config_path)
    name = args.name or store["active_profile"]
    if not name:
        raise SystemExit("No active profile. Run the setup skill first.")
    if name not in store["profiles"]:
        raise SystemExit(f"Unknown profile {name!r}.")
    output = {"name": name, "active": name == store["active_profile"], **store["profiles"][name]}
    print(json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True))


def command_activate(args: argparse.Namespace) -> None:
    store = load_store(args.config_path)
    if args.name not in store["profiles"]:
        raise SystemExit(f"Unknown profile {args.name!r}.")
    store["active_profile"] = args.name
    atomic_write(args.config_path, store)
    print(json.dumps({"active_profile": args.name, "path": str(args.config_path)}))


def command_validate(args: argparse.Namespace) -> None:
    store = load_store(args.config_path)
    validate_store(store)
    print(json.dumps({"valid": True, "profiles": len(store["profiles"]), "active_profile": store["active_profile"]}))


def add_common_config_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config-path", type=Path, default=DEFAULT_CONFIG_PATH)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage tracking-event QA profiles without credentials.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    save = subparsers.add_parser("save", help="Create or update a profile.")
    add_common_config_argument(save)
    save.add_argument("--name", required=True)
    save.add_argument("--squad", required=True)
    save.add_argument("--product", required=True)
    save.add_argument("--notion-source", required=True)
    save.add_argument("--posthog-project-id", required=True)
    save.add_argument("--posthog-project-name", default="PostHog project")
    save.add_argument("--jira-project-key")
    save.add_argument("--jira-issue-type", default="Task")
    save.add_argument("--event-name-property", default="Event Name")
    save.add_argument("--app-status-property", default="App Status")
    save.add_argument("--web-status-property", default="Web Status")
    save.add_argument("--tracking-platform-property", default="Tracking Platform")
    save.add_argument("--assignee-property", default="Assignee")
    save.add_argument("--last-verified-property", default="Last Verified")
    save.add_argument("--verification-note-property", default="Verification Note")
    save.add_argument("--reproduce-link-property", default="PostHog Reproduce Link")
    save.add_argument("--qa-value", default="QA")
    save.add_argument("--live-value", default="Live")
    save.add_argument("--platform-property", default="$lib")
    save.add_argument(
        "--platform-values-json",
        type=parse_platform_values,
        help='Observed mapping as JSON, for example {"web":["web"],"app":["mobile"]}.',
    )
    save.add_argument("--lookback-days", type=int, default=90)
    save.add_argument("--recency-days", type=int, default=14)
    save.add_argument("--live-volume", type=int, default=10)
    save.add_argument("--activate", action="store_true")
    save.add_argument("--replace", action="store_true", help="Replace an existing profile with the same name.")
    save.set_defaults(func=command_save)

    listing = subparsers.add_parser("list", help="List profiles.")
    add_common_config_argument(listing)
    listing.add_argument("--json", action="store_true")
    listing.set_defaults(func=command_list)

    show = subparsers.add_parser("show", help="Show a profile, defaulting to the active profile.")
    add_common_config_argument(show)
    show.add_argument("--name")
    show.set_defaults(func=command_show)

    activate = subparsers.add_parser("activate", help="Set the active profile.")
    add_common_config_argument(activate)
    activate.add_argument("name")
    activate.set_defaults(func=command_activate)

    validate = subparsers.add_parser("validate", help="Validate the profile store.")
    add_common_config_argument(validate)
    validate.set_defaults(func=command_validate)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
