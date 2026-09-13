from __future__ import annotations

import json
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "manage_profiles.py"


class ManageProfilesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.config_path = Path(self.temp_dir.name) / "profiles.json"

    def save_command(self, *extra: str) -> list[str]:
        return [
            sys.executable,
            str(SCRIPT),
            "save",
            "--config-path",
            str(self.config_path),
            "--name",
            "sample-profile",
            "--squad",
            "Sample Squad",
            "--product",
            "Sample Product",
            "--notion-source",
            "collection://sample-source",
            "--posthog-project-id",
            "sample-project",
            *extra,
        ]

    def stream_command(self, *extra: str) -> list[str]:
        return self.save_command(
            "--stream-dataset",
            "sample-stream",
            "--stream-platform-field",
            "source",
            "--stream-platform-values-json",
            json.dumps({"web": ["example.test"], "app": ["app.example.test"]}),
            *extra,
        )

    def run_command(self, command: list[str], *, succeeds: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if succeeds and result.returncode != 0:
            self.fail(f"Command failed: {result.stderr or result.stdout}")
        return result

    def read_profile(self) -> dict:
        store = json.loads(self.config_path.read_text(encoding="utf-8"))
        return store["profiles"]["sample-profile"]

    def test_saves_observed_platform_mapping_with_private_permissions(self) -> None:
        mapping = {"web": ["client-web"], "app": ["client-mobile"]}
        self.run_command(
            self.save_command("--platform-values-json", json.dumps(mapping), "--activate")
        )

        store = json.loads(self.config_path.read_text(encoding="utf-8"))
        profile = store["profiles"]["sample-profile"]
        self.assertEqual(profile["posthog"]["platform_values"], mapping)
        self.assertEqual(store["active_profile"], "sample-profile")
        self.assertEqual(stat.S_IMODE(self.config_path.stat().st_mode), 0o600)

    def test_existing_profile_requires_replace(self) -> None:
        self.run_command(self.save_command())
        rejected = self.run_command(self.save_command(), succeeds=False)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("already exists", rejected.stderr)

        self.run_command(self.save_command("--replace"))

    def test_recency_must_fit_inside_lookback(self) -> None:
        rejected = self.run_command(
            self.save_command("--lookback-days", "30", "--recency-days", "31"),
            succeeds=False,
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("recency_days <= lookback_days", rejected.stderr)

    def test_platform_mapping_needs_an_observed_value(self) -> None:
        rejected = self.run_command(
            self.save_command("--platform-values-json", '{"web":[]}'),
            succeeds=False,
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("at least one mapped platform value", rejected.stderr)

    def test_profile_without_stream_channel_stays_valid(self) -> None:
        self.run_command(self.save_command())
        self.assertNotIn("stream", self.read_profile())
        validated = self.run_command(
            [sys.executable, str(SCRIPT), "validate", "--config-path", str(self.config_path)]
        )
        self.assertIn('"profiles_with_stream_channel": 0', validated.stdout)

    def test_saves_stream_channel_with_key_value_shape(self) -> None:
        self.run_command(
            self.stream_command(
                "--stream-property-key-field",
                "data_key",
                "--stream-property-value-field",
                "string_value",
                "--stream-key-prefixes-json",
                json.dumps({"web": "attributes.", "app": ""}),
                "--stream-excluded-values",
                "staging.example.test, localhost",
            )
        )

        stream = self.read_profile()["stream"]
        self.assertEqual(stream["dataset"], "sample-stream")
        self.assertEqual(stream["platform_values"]["app"], ["app.example.test"])
        self.assertEqual(stream["property_key_prefixes"], {"web": "attributes.", "app": ""})
        self.assertEqual(stream["excluded_platform_values"], ["staging.example.test", "localhost"])

    def test_stream_key_field_requires_a_value_field(self) -> None:
        rejected = self.run_command(
            self.stream_command("--stream-property-key-field", "data_key"),
            succeeds=False,
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("stream.property_value_field", rejected.stderr)

    def test_stream_cannot_exclude_a_mapped_platform_value(self) -> None:
        rejected = self.run_command(
            self.stream_command("--stream-excluded-values", "app.example.test"),
            succeeds=False,
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("excludes mapped platform values", rejected.stderr)

    def test_stream_platform_mapping_must_use_supported_platforms(self) -> None:
        rejected = self.run_command(
            self.save_command(
                "--stream-dataset",
                "sample-stream",
                "--stream-platform-values-json",
                '{"kiosk":["kiosk.example.test"]}',
            ),
            succeeds=False,
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("unsupported", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
