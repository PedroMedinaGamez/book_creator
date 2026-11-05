#!/usr/bin/env python3
"""Generate, normalize, and version a complete Bo interior page."""

from __future__ import annotations

import argparse
import base64
import binascii
import io
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps


API_URL = "https://api.openai.com/v1/images/edits"
DEFAULT_MODEL = "gpt-image-2.5-sunburst"
DEFAULT_SIZE = "2496x3232"
OUTPUT_SIZE = (2550, 3300)
OUTPUT_DPI = (300, 300)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_DATA_URL_LENGTH = 20_971_520
PAGE_FILENAME = re.compile(r"^page_(\d+)\.v(\d+)\.png$")
SUPPORTED_IMAGES = {
    ".jpg": ("image/jpeg", b"\xff\xd8\xff"),
    ".jpeg": ("image/jpeg", b"\xff\xd8\xff"),
    ".png": ("image/png", PNG_SIGNATURE),
    ".webp": ("image/webp", b"RIFF"),
}


def safe_slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    if not slug:
        raise ValueError("El continente debe incluir letras o números.")
    return slug


def read_image_data_url(path: Path) -> str:
    try:
        image_bytes = path.read_bytes()
    except OSError as error:
        raise ValueError(f"No se pudo leer la imagen de referencia {path}: {error}") from None

    image_type = SUPPORTED_IMAGES.get(path.suffix.lower())
    if image_type is None or not image_bytes.startswith(image_type[1]):
        raise ValueError(f"La imagen de referencia no es válida: {path}")

    data_url = (
        f"data:{image_type[0]};base64,"
        f"{base64.b64encode(image_bytes).decode('ascii')}"
    )
    if len(data_url) > MAX_DATA_URL_LENGTH:
        raise ValueError(f"La imagen supera el límite permitido por la API: {path}")
    return data_url


def validate_prompt(prompt: str, expected_text: str) -> None:
    expected_text = expected_text.rstrip("\r\n")
    if not prompt.strip() or not expected_text:
        raise ValueError("Se requieren un prompt y el texto aprobado.")
    unresolved_markers = (
        "[Inserta el texto",
        "<TEXTO_DE_LA_PAGINA>",
        "[PAGE_TEXT]",
        "[Insert the complete approved text",
    )
    if any(marker in prompt for marker in unresolved_markers):
        raise ValueError("El prompt todavía contiene un marcador sin completar.")
    if expected_text not in prompt:
        raise ValueError(
            "El prompt no contiene literalmente todo el texto aprobado de la página."
        )


def build_payload(
    prompt: str,
    illustration: Path,
    previous_page: Path | None,
    model: str,
    size: str,
    style_reference: Path | None = None,
) -> dict[str, object]:
    images = [read_image_data_url(illustration)]
    if previous_page is not None:
        images.append(read_image_data_url(previous_page))
    if style_reference is not None:
        images.append(read_image_data_url(style_reference))
    return {
        "model": model,
        "images": [{"image_url": image} for image in images],
        "prompt": prompt,
        "size": size,
        "quality": "high",
        "output_format": "png",
        "background": "opaque",
        "n": 1,
    }


def request_page(payload: dict[str, object], api_key: str) -> bytes:
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
        raise RuntimeError(
            f"La API devolvió una respuesta JSON no válida: {error}"
        ) from None

    if not isinstance(response_data, dict):
        raise RuntimeError("La API devolvió una respuesta JSON inesperada.")
    data = response_data.get("data")
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        raise RuntimeError("La API no devolvió ninguna página.")
    encoded = data[0].get("b64_json")
    if not isinstance(encoded, str):
        raise RuntimeError("La respuesta no incluye la imagen PNG esperada.")
    try:
        image_bytes = base64.b64decode(encoded, validate=True)
    except (ValueError, binascii.Error) as error:
        raise RuntimeError(f"La imagen devuelta no es base64 válido: {error}") from None
    if not image_bytes.startswith(PNG_SIGNATURE):
        raise RuntimeError("La API no devolvió un PNG válido.")
    return image_bytes


def normalize_page(image_bytes: bytes) -> bytes:
    try:
        with Image.open(io.BytesIO(image_bytes)) as source:
            source.load()
            image = ImageOps.exif_transpose(source).convert("RGB")
    except (OSError, ValueError) as error:
        raise ValueError(f"No se pudo decodificar la página PNG: {error}") from None

    target_ratio = OUTPUT_SIZE[0] / OUTPUT_SIZE[1]
    source_ratio = image.width / image.height
    if abs(source_ratio - target_ratio) / target_ratio > 0.015:
        raise ValueError(
            "La proporción de la página generada se desvía más de 1.5% "
            "del formato vertical aprobado; no se recortará ni deformará."
        )

    contained = ImageOps.contain(
        image, OUTPUT_SIZE, method=Image.Resampling.LANCZOS
    )
    canvas = Image.new("RGB", OUTPUT_SIZE, "white")
    canvas.paste(
        contained,
        ((OUTPUT_SIZE[0] - contained.width) // 2, (OUTPUT_SIZE[1] - contained.height) // 2),
    )
    buffer = io.BytesIO()
    canvas.save(buffer, format="PNG", dpi=OUTPUT_DPI, optimize=True)
    return buffer.getvalue()


def next_page_version(directory: Path, page_number: int) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    highest_version = 0
    for candidate in directory.iterdir():
        match = PAGE_FILENAME.fullmatch(candidate.name)
        if match and int(match.group(1)) == page_number:
            highest_version = max(highest_version, int(match.group(2)))
    return directory / f"page_{page_number}.v{highest_version + 1}.png"


def save_page(
    image_bytes: bytes, pages_root: Path, continent: str, page_number: int
) -> Path:
    if not image_bytes.startswith(PNG_SIGNATURE):
        raise ValueError("La página que se va a guardar no es un PNG válido.")
    directory = pages_root / safe_slug(continent)
    while True:
        destination = next_page_version(directory, page_number)
        try:
            with destination.open("xb") as page_file:
                page_file.write(image_bytes)
            return destination
        except FileExistsError:
            continue


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Genera una página interior y la guarda como "
            "pages/<continente>/page_<N>.vN.png."
        )
    )
    parser.add_argument("--prompt-file", required=True, type=Path)
    parser.add_argument("--expected-text-file", required=True, type=Path)
    parser.add_argument("--illustration", required=True, type=Path)
    parser.add_argument("--continent", required=True)
    parser.add_argument("--page-number", required=True, type=int)
    parser.add_argument("--previous-page", type=Path)
    parser.add_argument(
        "--style-reference",
        type=Path,
        help="Imagen adicional de referencia para conservar la tipograf?a o el estilo.",
    )
    parser.add_argument("--pages-root", type=Path, default=Path("pages"))
    parser.add_argument(
        "--model", default=os.environ.get("OPENAI_IMAGE_MODEL", DEFAULT_MODEL)
    )
    parser.add_argument("--size", default=DEFAULT_SIZE)
    parser.add_argument(
        "--confirm-paid-request",
        action="store_true",
        help="Confirma la autorización del usuario para esta llamada facturable.",
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
    if args.page_number < 1:
        print("Error: el número de página debe ser positivo.", file=sys.stderr)
        return 2

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(
            "Error: configura OPENAI_API_KEY localmente; no la compartas en el chat.",
            file=sys.stderr,
        )
        return 2

    try:
        prompt = args.prompt_file.read_text(encoding="utf-8")
        expected_text = args.expected_text_file.read_text(encoding="utf-8")
        validate_prompt(prompt, expected_text)
        payload = build_payload(
            prompt,
            args.illustration,
            args.previous_page,
            args.model,
            args.size,
            args.style_reference,
        )
        generated_bytes = request_page(payload, api_key)
        normalized_bytes = normalize_page(generated_bytes)
        output_path = save_page(
            normalized_bytes, args.pages_root, args.continent, args.page_number
        )
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(output_path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
