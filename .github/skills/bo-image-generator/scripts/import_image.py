#!/usr/bin/env python3
"""Import a ChatGPT-generated PNG into the versioned images directory."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import unicodedata
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def safe_slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    if not slug:
        raise ValueError("Continente, país y monumento deben incluir letras o números.")
    return slug


def import_next_version(
    source: Path,
    output_root: Path,
    continent: str,
    country: str,
    monument: str,
) -> Path:
    try:
        with source.open("rb") as source_file:
            if source_file.read(len(PNG_SIGNATURE)) != PNG_SIGNATURE:
                raise ValueError("El archivo descargado no es un PNG válido.")
    except OSError as error:
        raise ValueError(f"No se pudo leer la imagen descargada: {error}") from None

    destination = output_root / safe_slug(continent) / safe_slug(country)
    destination.mkdir(parents=True, exist_ok=True)
    monument_slug = safe_slug(monument)

    version = 1
    while True:
        path = destination / f"{monument_slug}_v{version}.png"
        try:
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
        except FileExistsError:
            version += 1
            continue

        try:
            with source.open("rb") as source_file, os.fdopen(
                descriptor, "wb"
            ) as destination_file:
                shutil.copyfileobj(source_file, destination_file)
        except BaseException:
            path.unlink(missing_ok=True)
            raise
        return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Importa un PNG generado en ChatGPT a images/<continente>/<país>/."
    )
    parser.add_argument("--source", required=True, type=Path, help="PNG descargado de ChatGPT.")
    parser.add_argument("--continent", required=True)
    parser.add_argument("--country", required=True)
    parser.add_argument("--monument", required=True)
    parser.add_argument("--output-root", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        output_root = args.output_root
        if output_root is None:
            repository_root = Path(__file__).resolve().parents[4]
            output_root = repository_root / "images"
        output_path = import_next_version(
            args.source,
            output_root,
            args.continent,
            args.country,
            args.monument,
        )
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(output_path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
