import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

import format_interior


def write_page(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", format_interior.EXPECTED_SIZE, "white").save(
        path, format="PNG", dpi=format_interior.EXPECTED_DPI, optimize=True
    )


class FormatInteriorTests(unittest.TestCase):
    def test_uses_latest_approved_versions_and_inserts_blank_pages(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            pages_root = root / "pages"
            page_directory = pages_root / "europe"
            write_page(page_directory / "page_1.v1.png")
            write_page(page_directory / "page_1.v2.png")
            write_page(page_directory / "page_2.v1.png")
            manifest = root / "qa.json"
            manifest.write_text(
                json.dumps(
                    {
                        "pages": {
                            "1": {"status": "PASS", "version": 2},
                            "2": {
                                "status": "PASS WITH NOTES",
                                "version": 1,
                                "user_accepted_notes": True,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            arguments = [
                "format_interior.py",
                "--continent",
                "Europe",
                "--page-count",
                "2",
                "--qa-manifest",
                str(manifest),
                "--pages-root",
                str(pages_root),
            ]
            with patch.object(sys, "argv", arguments):
                with contextlib.redirect_stdout(io.StringIO()):
                    result = format_interior.main()

            pdf_path = page_directory / "Bo_KDP_Interior_8.5x11.pdf"
            report_path = page_directory / "Bo_KDP_Preflight_Report.txt"
            self.assertEqual(result, 0)
            pdf_data = pdf_path.read_bytes()
            self.assertTrue(pdf_data.startswith(b"%PDF-"))
            self.assertEqual(
                len(format_interior.re.findall(rb"/Type\s*/Page\b", pdf_data)), 3
            )
            report_text = report_path.read_text(encoding="utf-8")
            self.assertIn("Página 1: v2", report_text)
            self.assertIn("Página 2: v1", report_text)

    def test_rejects_newer_page_version_without_matching_qa_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            page_directory = root / "pages" / "europe"
            write_page(page_directory / "page_1.v1.png")
            write_page(page_directory / "page_1.v2.png")
            manifest = root / "qa.json"
            manifest.write_text(
                json.dumps({"pages": {"1": {"status": "PASS", "version": 1}}}),
                encoding="utf-8",
            )
            arguments = [
                "format_interior.py",
                "--continent",
                "Europe",
                "--page-count",
                "1",
                "--qa-manifest",
                str(manifest),
                "--pages-root",
                str(root / "pages"),
            ]
            with patch.object(sys, "argv", arguments):
                with contextlib.redirect_stderr(io.StringIO()):
                    result = format_interior.main()

            self.assertEqual(result, 1)
            self.assertFalse((page_directory / "Bo_KDP_Interior_8.5x11.pdf").exists())

    def test_rejects_missing_expected_page(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            page_directory = Path(temporary_directory) / "europe"
            with self.assertRaisesRegex(ValueError, "No hay archivo final"):
                format_interior.find_latest_page(page_directory, 2)

    def test_pdf_generation_does_not_follow_predictable_temp_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            output_path = root / "Bo_KDP_Interior_8.5x11.pdf"
            sentinel = root / "sentinel.txt"
            sentinel.write_text("unchanged", encoding="utf-8")
            predictable_temp_path = root / "Bo_KDP_Interior_8.5x11.tmp.pdf"
            try:
                predictable_temp_path.symlink_to(sentinel)
            except (NotImplementedError, OSError):
                self.skipTest("El sistema no permite crear symlinks sin privilegios.")

            page = Image.new("RGB", format_interior.EXPECTED_SIZE, "white")
            format_interior.build_pdf([page], output_path)

            self.assertEqual(sentinel.read_text(encoding="utf-8"), "unchanged")
            self.assertTrue(predictable_temp_path.is_symlink())
            self.assertTrue(output_path.read_bytes().startswith(b"%PDF-"))


if __name__ == "__main__":
    unittest.main()
