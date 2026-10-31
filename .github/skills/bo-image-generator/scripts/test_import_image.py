import tempfile
import unittest
from pathlib import Path

import import_image


PNG_BYTES = b"\x89PNG\r\n\x1a\nillustration"


class ImportImageTests(unittest.TestCase):
    def test_imports_incrementing_versions_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "chatgpt-download.png"
            source.write_bytes(PNG_BYTES)
            output_root = root / "images"

            first = import_image.import_next_version(
                source, output_root, "Asia", "Japan", "Himeji Castle"
            )
            second = import_image.import_next_version(
                source, output_root, "Asia", "Japan", "Himeji Castle"
            )

            self.assertEqual(
                first.relative_to(output_root).as_posix(),
                "asia/japan/v1/himeji-castle.png",
            )
            self.assertEqual(
                second.relative_to(output_root).as_posix(),
                "asia/japan/v2/himeji-castle.png",
            )
            self.assertEqual(first.read_bytes(), PNG_BYTES)
            self.assertEqual(second.read_bytes(), PNG_BYTES)

    def test_different_monuments_share_version_directory_without_colliding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "chatgpt-download.png"
            source.write_bytes(PNG_BYTES)
            output_root = root / "images"

            first = import_image.import_next_version(
                source, output_root, "Asia", "Japan", "Himeji Castle"
            )
            second = import_image.import_next_version(
                source, output_root, "Asia", "Japan", "Mount Fuji"
            )

            self.assertEqual(first.parent, second.parent)
            self.assertEqual(first.parent.name, "v1")
            self.assertEqual(second.name, "mount-fuji.png")

    def test_rejects_non_png_without_creating_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "image.jpg"
            source.write_bytes(b"\xff\xd8\xffnot a PNG")
            output_root = root / "images"

            with self.assertRaisesRegex(ValueError, "no es un PNG"):
                import_image.import_next_version(
                    source, output_root, "Asia", "Japan", "Himeji Castle"
                )

            self.assertFalse(output_root.exists())


if __name__ == "__main__":
    unittest.main()
