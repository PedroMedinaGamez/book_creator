#!/usr/bin/env python3
"""Generate and version a Bo illustration using the OpenAI Images API."""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


API_URL = "https://api.openai.com/v1/images/edits"
DEFAULT_MODEL = "gpt-image-2.5-sunburst"
MAX_DATA_URL_LENGTH = 20_971_520
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SUPPORTED_IMAGE_TYPES = {
    ".jpg": ("image/jpeg", b"\xff\xd8\xff"),
    ".jpeg": ("image/jpeg", b"\xff\xd8\xff"),
    ".png": ("image/png", PNG_SIGNATURE),
    ".webp": ("image/webp", b"RIFF"),
}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def read_image_data_url(path: Path) -> str:
    try:
        image_bytes = path.read_bytes()
    except OSError as error:
        raise ValueError(f"No se pudo leer la imagen de referencia: {error}") from None

    image_type = SUPPORTED_IMAGE_TYPES.get(path.suffix.lower())
    if image_type is None or not image_bytes.startswith(image_type[1]):
        raise ValueError(
            f"La imagen de referencia no es un archivo PNG, JPEG o WebP válido: {path}"
        )

    encoded = base64.b64encode(image_bytes).decode("ascii")
    data_url = f"data:{image_type[0]};base64,{encoded}"
    if len(data_url) > MAX_DATA_URL_LENGTH:
        raise ValueError(f"La imagen de referencia supera el límite de la API: {path}")
    return data_url


def build_request_payload(
    prompt: str,
    reference_images: list[Path],
    model: str,
    size: str,
    quality: str,
) -> dict[str, object]:
    if not prompt.strip():
        raise ValueError("El prompt no puede estar vacío.")
    if not reference_images:
        raise ValueError("Se requiere al menos una imagen de referencia.")

    images = [
        {"image_url": read_image_data_url(image_path)}
        for image_path in reference_images
    ]
    return {
        "model": model,
        "images": images,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "output_format": "png",
        "background": "opaque",
        "n": 1,
    }


def request_image(payload: dict[str, object], api_key: str) -> bytes:
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"La API de OpenAI devolvió HTTP {error.code}: {error_body}"
        ) from None
    except urllib.error.URLError as error:
        raise RuntimeError(
            f"No se pudo conectar con la API de OpenAI: {error.reason}"
        ) from None
    except OSError as error:
        raise RuntimeError(f"Falló la conexión con la API de OpenAI: {error}") from None
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"La API devolvió una respuesta JSON no válida: {error}") from None

    if not isinstance(response_data, dict):
        raise RuntimeError("La API devolvió una respuesta JSON con formato inesperado.")
    data = response_data.get("data")
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        raise RuntimeError("La API no devolvió ninguna imagen.")
    image_base64 = data[0].get("b64_json")
    if not isinstance(image_base64, str):
        raise RuntimeError("La respuesta de la API no contiene la imagen PNG esperada.")

    try:
        image_bytes = base64.b64decode(image_base64, validate=True)
    except (ValueError, binascii.Error) as error:
        raise RuntimeError(f"La imagen devuelta no es base64 válido: {error}") from None
    if not image_bytes.startswith(PNG_SIGNATURE):
        raise RuntimeError("La respuesta de la API no contiene un PNG válido.")
    return image_bytes


def parse_args() -> argparse.Namespace:
    root = repository_root()
    parser = argparse.ArgumentParser(
        description=(
            "Genera una ilustración con la API de OpenAI y la guarda "
            "en images/<continente>/<país>/vN/<monumento>.png."
        )
    )
    prompt_source = parser.add_mutually_exclusive_group(required=True)
    prompt_source.add_argument("--prompt", help="Prompt final de bo-page-artist.")
    prompt_source.add_argument(
        "--prompt-file", type=Path, help="Archivo UTF-8 con el prompt final."
    )
    parser.add_argument("--continent", required=True)
    parser.add_argument("--country", required=True)
    parser.add_argument("--monument", required=True)
    parser.add_argument(
        "--reference",
        type=Path,
        default=root / "Bo_image.jpg",
        help="Imagen maestra de Bo (por defecto: Bo_image.jpg en la raíz).",
    )
    parser.add_argument(
        "--previous-image",
        type=Path,
        help="Versión anterior que se usará como referencia para una corrección.",
    )
    parser.add_argument("--output-root", type=Path, default=root / "images")
    parser.add_argument(
        "--model", default=os.environ.get("OPENAI_IMAGE_MODEL", DEFAULT_MODEL)
    )
    parser.add_argument("--size", default="1024x1536")
    parser.add_argument(
        "--quality",
        choices=("low", "medium", "high", "xhigh", "max"),
        default="high",
    )
    parser.add_argument(
        "--confirm-paid-request",
        action="store_true",
        help="Confirma que el usuario autorizó esta solicitud facturable.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.confirm_paid_request:
        print(
            "Error: confirma la solicitud facturable con --confirm-paid-request.",
            file=sys.stderr,
        )
        return 2

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(
            "Error: configura OPENAI_API_KEY en el entorno local; no la compartas en el chat.",
            file=sys.stderr,
        )
        return 2

    try:
        if args.prompt_file is not None:
            prompt = args.prompt_file.read_text(encoding="utf-8")
        else:
            prompt = args.prompt or ""

        reference_images = [args.reference]
        if args.previous_image is not None:
            reference_images.append(args.previous_image)
        payload = build_request_payload(
            prompt, reference_images, args.model, args.size, args.quality
        )
        scripts_dir = (
            repository_root()
            / ".github"
            / "skills"
            / "bo-image-generator"
            / "scripts"
        )
        sys.path.insert(0, str(scripts_dir))
        try:
            from import_image import save_png_next_version
        except ImportError as error:
            raise RuntimeError(
                "No se pudo cargar el guardado versionado de imágenes."
            ) from error

        image_bytes = request_image(payload, api_key)
        output_path = save_png_next_version(
            image_bytes,
            args.output_root,
            args.continent,
            args.country,
            args.monument,
        )
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(output_path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
