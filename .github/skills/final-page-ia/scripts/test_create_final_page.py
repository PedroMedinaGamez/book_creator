import base64
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

import create_final_page


def png_bytes(size: tuple[int, int] = (64, 80)) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", size, "white").save(buffer, format="PNG")
    return buffer.getvalue()


class FinalPageTests(unittest.TestCase):
    def test_requires_exact_approved_text_inside_complete_prompt(self) -> None:
        create_final_page.validate_prompt(
            "Layout this page.\n<TEXTO>\nBo mira el castillo.\n</TEXTO>",
            "Bo mira el castillo.\n",
        )
        with self.assertRaisesRegex(ValueError, "no contiene literalmente"):
            create_final_page.validate_prompt(
                "Layout this page. Bo mira el castillo",
                "Bo mira el castillo.",
            )
        with self.assertRaisesRegex(ValueError, "marcador"):
            create_final_page.validate_prompt(
                "Layout this page. [Inserta el texto aprobado]",
                "Approved text",
            )

    def test_payload_uses_compiler_illustration_and_previous_page(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            illustration = root / "approved-illustration.png"
            previous_page = root / "page_7.v2.png"
            style_reference = root / "page_6.v3.png"
            illustration.write_bytes(png_bytes())
            previous_page.write_bytes(png_bytes())
            style_reference.write_bytes(png_bytes())

            payload = create_final_page.build_payload(
                "Exact page prompt",
                illustration,
                previous_page,
                "gpt-image-2.5-sunburst",
                "2496x3232",
                style_reference=style_reference,
            )

        self.assertEqual(payload["prompt"], "Exact page prompt")
        self.assertEqual(payload["size"], "2496x3232")
        self.assertEqual(len(payload["images"]), 3)

    def test_normalizes_page_without_changing_portrait_layout(self) -> None:
        normalized_bytes = create_final_page.normalize_page(png_bytes((2496, 3232)))
        with Image.open(io.BytesIO(normalized_bytes)) as normalized:
            self.assertEqual(normalized.size, create_final_page.OUTPUT_SIZE)
            self.assertAlmostEqual(normalized.info["dpi"][0], 300, delta=1)
            self.assertAlmostEqual(normalized.info["dpi"][1], 300, delta=1)

    def test_rejects_extreme_aspect_ratio_instead_of_cropping(self) -> None:
        with self.assertRaisesRegex(ValueError, "se desvía más de 1.5%"):
            create_final_page.normalize_page(png_bytes((64, 64)))

    def test_saves_incrementing_versions_by_page_number(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            pages_root = Path(temporary_directory)
            first = create_final_page.save_page(png_bytes(), pages_root, "Europe", 3)
            second = create_final_page.save_page(png_bytes(), pages_root, "Europe", 3)

            self.assertEqual(first.name, "page_3.v1.png")
            self.assertEqual(second.name, "page_3.v2.png")
            self.assertEqual(first.parent.name, "europe")

    def test_request_page_decodes_png_response(self) -> None:
        expected_png = png_bytes()
        response = json.dumps(
            {"data": [{"b64_json": base64.b64encode(expected_png).decode("ascii")}]}
        ).encode("utf-8")
        with patch(
            "create_final_page.urllib.request.urlopen",
            return_value=io.BytesIO(response),
        ) as urlopen:
            result = create_final_page.request_page({"prompt": "Test"}, "test-secret")

        self.assertEqual(result, expected_png)
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, create_final_page.API_URL)
        self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")


if __name__ == "__main__":
    unittest.main()
