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

    def run_command(self, command: list[str], *, succeeds: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if succeeds and result.returncode != 0:
            self.fail(f"Command failed: {result.stderr or result.stdout}")
        return result

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


if __name__ == "__main__":
    unittest.main()
