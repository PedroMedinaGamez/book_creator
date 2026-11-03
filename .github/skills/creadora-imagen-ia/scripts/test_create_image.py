import base64
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

import create_image


JPEG_BYTES = b"\xff\xd8\xffreference"


def make_png(size: tuple[int, int], color: str = "black") -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", size, color).save(buffer, format="PNG")
    return buffer.getvalue()


API_PNG_BYTES = make_png(create_image.API_IMAGE_DIMENSIONS)


class CreateImageTests(unittest.TestCase):
    def test_model_default_does_not_read_another_environment_variable(self) -> None:
        arguments = [
            "create_image.py",
            "--prompt",
            "Approved prompt",
            "--continent",
            "Asia",
            "--country",
            "Not applicable",
            "--monument",
            "Opening",
        ]
        with patch.object(sys, "argv", arguments):
            with patch.dict(os.environ, {"OPENAI_IMAGE_MODEL": "unexpected-model"}):
                args = create_image.parse_args()

        self.assertEqual(args.model, create_image.DEFAULT_MODEL)
        self.assertEqual(args.size, create_image.API_IMAGE_SIZE)

    def test_builds_edit_payload_with_reference_and_exact_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            reference = Path(temporary_directory) / "Bo_image.jpg"
            reference.write_bytes(JPEG_BYTES)

            payload = create_image.build_request_payload(
                "Exact artist prompt", [reference], "gpt-image-2.5-sunburst",
                create_image.API_IMAGE_SIZE, "high"
            )

        self.assertEqual(payload["prompt"], "Exact artist prompt")
        self.assertEqual(payload["model"], "gpt-image-2.5-sunburst")
        self.assertEqual(payload["output_format"], "png")
        self.assertEqual(payload["size"], create_image.API_IMAGE_SIZE)
        self.assertEqual(
            payload["images"],
            [
                {
                    "image_url": "data:image/jpeg;base64,"
                    + base64.b64encode(JPEG_BYTES).decode("ascii")
                }
            ],
        )

    def test_request_image_decodes_png_response(self) -> None:
        response_body = json.dumps(
            {"data": [{"b64_json": base64.b64encode(API_PNG_BYTES).decode("ascii")}]}
        ).encode("utf-8")
        payload = {"prompt": "A test image"}

        with patch(
            "create_image.urllib.request.urlopen",
            return_value=io.BytesIO(response_body),
        ) as urlopen:
            image_bytes = create_image.request_image(payload, "test-secret")

        with Image.open(io.BytesIO(image_bytes)) as image:
            self.assertEqual(image.size, create_image.ILLUSTRATION_DIMENSIONS)
            self.assertEqual(image.getpixel((0, 0)), (255, 255, 255))
            self.assertEqual(image.getpixel((0, 30)), (0, 0, 0))
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, create_image.API_URL)
        self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")

    def test_rejects_missing_or_invalid_reference_image(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            reference = Path(temporary_directory) / "reference.jpg"
            reference.write_bytes(b"not an image")

            with self.assertRaisesRegex(ValueError, "no es un archivo"):
                create_image.read_image_data_url(reference)

    def test_rejects_non_png_api_response(self) -> None:
        response_body = json.dumps(
            {"data": [{"b64_json": base64.b64encode(b"not png").decode("ascii")}]}
        ).encode("utf-8")

        with patch(
            "create_image.urllib.request.urlopen",
            return_value=io.BytesIO(response_body),
        ):
            with self.assertRaisesRegex(RuntimeError, "PNG válido"):
                create_image.request_image({"prompt": "A test image"}, "test-secret")

    def test_rejects_api_image_with_different_dimensions(self) -> None:
        image_bytes = make_png((1024, 1536))
        response_body = json.dumps(
            {"data": [{"b64_json": base64.b64encode(image_bytes).decode("ascii")}]}
        ).encode("utf-8")

        with patch(
            "create_image.urllib.request.urlopen",
            return_value=io.BytesIO(response_body),
        ):
            with self.assertRaisesRegex(RuntimeError, "se requieren 1024x1024"):
                create_image.request_image({"prompt": "A test image"}, "test-secret")

    def test_rejects_custom_image_size(self) -> None:
        arguments = [
            "create_image.py",
            "--prompt",
            "Approved prompt",
            "--continent",
            "Asia",
            "--country",
            "Japan",
            "--monument",
            "Mount Fuji",
            "--size",
            "1024x1536",
        ]
        with patch.object(sys, "argv", arguments):
            with self.assertRaises(SystemExit):
                create_image.parse_args()

    def test_paid_request_requires_explicit_confirmation(self) -> None:
        arguments = [
            "create_image.py",
            "--prompt",
            "Approved prompt",
            "--continent",
            "Europe",
            "--country",
            "France",
            "--monument",
            "Eiffel Tower",
        ]
        with patch.object(sys, "argv", arguments):
            with patch.dict(os.environ, {}, clear=True):
                with patch("create_image.urllib.request.urlopen") as urlopen:
                    with contextlib.redirect_stderr(io.StringIO()):
                        result = create_image.main()

        self.assertEqual(result, 2)
        urlopen.assert_not_called()

    def test_main_saves_api_png_to_first_version_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            reference = root / "Bo_image.jpg"
            reference.write_bytes(JPEG_BYTES)
            output_root = root / "images"
            response_body = json.dumps(
                {
                    "data": [
                        {
                            "b64_json": base64.b64encode(
                                API_PNG_BYTES
                            ).decode("ascii")
                        }
                    ]
                }
            ).encode("utf-8")
            arguments = [
                "create_image.py",
                "--prompt",
                "Approved prompt",
                "--continent",
                "Asia",
                "--country",
                "Japan",
                "--monument",
                "Himeji Castle",
                "--reference",
                str(reference),
                "--output-root",
                str(output_root),
                "--confirm-paid-request",
            ]
            with patch.object(sys, "argv", arguments):
                with patch.dict(os.environ, {"OPENAI_API_KEY": "test-secret"}):
                    with patch(
                        "create_image.urllib.request.urlopen",
                        return_value=io.BytesIO(response_body),
                    ):
                        with contextlib.redirect_stdout(io.StringIO()):
                            result = create_image.main()

            generated_file = output_root / "asia" / "japan" / "v1" / "himeji-castle.png"
            self.assertEqual(result, 0)
            with Image.open(generated_file) as image:
                self.assertEqual(image.size, create_image.ILLUSTRATION_DIMENSIONS)


if __name__ == "__main__":
    unittest.main()
