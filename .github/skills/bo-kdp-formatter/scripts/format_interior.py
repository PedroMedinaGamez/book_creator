#!/usr/bin/env python3
"""Assemble the latest QA-approved page versions into an interleaved PDF."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

from PIL import Image


PAGE_FILE = re.compile(r"^page_(\d+)\.v(\d+)\.png$")
EXPECTED_SIZE = (2550, 3300)
EXPECTED_DPI = (300, 300)


def safe_slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    if not slug:
        raise ValueError("El continente debe incluir letras o números.")
    return slug


def read_qa_manifest(path: Path) -> dict[int, dict[str, object]]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"No se pudo leer el manifiesto QA: {error}") from None

    pages = manifest.get("pages") if isinstance(manifest, dict) else None
    if not isinstance(pages, dict):
        raise ValueError("El manifiesto QA debe contener un objeto 'pages'.")

    parsed_pages: dict[int, dict[str, object]] = {}
    for page_key, result in pages.items():
        try:
            page_number = int(page_key)
        except (TypeError, ValueError):
            raise ValueError(f"Número de página no válido en el manifiesto: {page_key}") from None
        if page_number < 1 or not isinstance(result, dict):
            raise ValueError(f"Resultado QA no válido para la página {page_key}.")
        parsed_pages[page_number] = result
    return parsed_pages


def find_unplanned_pages(pages_directory: Path, expected_count: int) -> list[int]:
    if not pages_directory.exists():
        return []
    try:
        page_numbers = {
            int(match.group(1))
            for candidate in pages_directory.iterdir()
            if candidate.is_file()
            for match in [PAGE_FILE.fullmatch(candidate.name)]
            if match
        }
    except OSError as error:
        raise ValueError(f"No se pudo comprobar el directorio de páginas: {error}") from None
    return sorted(page_numbers - set(range(1, expected_count + 1)))


def find_latest_page(
    pages_directory: Path, page_number: int
) -> tuple[int, Path]:
    versions: list[tuple[int, Path]] = []
    if not pages_directory.exists():
        raise ValueError(f"No hay archivo final para la página {page_number}.")
    try:
        candidates = pages_directory.iterdir()
        for candidate in candidates:
            match = PAGE_FILE.fullmatch(candidate.name)
            if candidate.is_file() and match and int(match.group(1)) == page_number:
                versions.append((int(match.group(2)), candidate))
    except OSError as error:
        raise ValueError(f"No se pudieron leer las versiones de página: {error}") from None

    if not versions:
        raise ValueError(f"No hay archivo final para la página {page_number}.")
    return max(versions, key=lambda version: version[0])


def validate_qa_approval(
    page_number: int, version: int, qa_result: dict[str, object] | None
) -> None:
    if qa_result is None:
        raise ValueError(f"Falta el resultado de auditoría para la página {page_number}.")
    status = qa_result.get("status")
    approved_version = qa_result.get("version")
    if approved_version != version:
        raise ValueError(
            f"La página {page_number} tiene una versión nueva (v{version}) "
            f"distinta de la auditada (v{approved_version}); vuelve a auditarla."
        )
    if status == "PASS":
        return
    if status == "PASS WITH NOTES" and qa_result.get("user_accepted_notes") is True:
        return
    raise ValueError(
        f"La página {page_number} v{version} no tiene aprobación QA: {status!r}."
    )


def inspect_page(path: Path) -> Image.Image:
    try:
        image = Image.open(path)
        image.load()
    except (OSError, ValueError) as error:
        raise ValueError(f"No se pudo abrir la página {path}: {error}") from None
    actual_size = image.size
    if actual_size != EXPECTED_SIZE:
        image.close()
        raise ValueError(
            f"{path} mide {actual_size[0]} × {actual_size[1]}; "
            f"se esperaba 2550 × 3300 píxeles."
        )
    dpi = image.info.get("dpi")
    if not isinstance(dpi, tuple) or len(dpi) < 2:
        image.close()
        raise ValueError(f"Faltan metadatos DPI en {path}.")
    if any(abs(actual - expected) > 1 for actual, expected in zip(dpi, EXPECTED_DPI)):
        image.close()
        raise ValueError(f"{path} no tiene metadatos de 300 DPI.")
    return image.convert("RGB")


def build_pdf(
    page_images: list[Image.Image], output_path: Path, resolution: int = 300
) -> int:
    if not page_images:
        raise ValueError("No hay páginas aprobadas para crear el PDF.")
    pdf_images: list[Image.Image] = []
    for index, page_image in enumerate(page_images):
        pdf_images.append(page_image.convert("RGB"))
        if index < len(page_images) - 1:
            pdf_images.append(Image.new("RGB", EXPECTED_SIZE, "white"))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{output_path.stem}.",
            suffix=".tmp.pdf",
            dir=output_path.parent,
        )
        temporary_path = Path(temporary_name)
        with os.fdopen(descriptor, "w+b") as pdf_file:
            pdf_images[0].save(
                pdf_file,
                format="PDF",
                save_all=True,
                append_images=pdf_images[1:],
                resolution=resolution,
            )
            pdf_file.flush()
            os.fsync(pdf_file.fileno())
            file_stat = os.fstat(pdf_file.fileno())
            path_stat = temporary_path.stat(follow_symlinks=False)
            if (
                temporary_path.is_symlink()
                or path_stat.st_dev != file_stat.st_dev
                or path_stat.st_ino != file_stat.st_ino
            ):
                raise OSError("El archivo PDF temporal fue sustituido de forma insegura.")
            if path_stat.st_size == 0:
                raise OSError("La exportación del PDF no creó un archivo válido.")
            pdf_file.seek(0)
            pdf_data = pdf_file.read()
            if not pdf_data.startswith(b"%PDF-"):
                raise OSError("El archivo exportado no tiene una cabecera PDF válida.")
        expected_page_count = len(pdf_images)
        actual_page_count = len(re.findall(rb"/Type\s*/Page\b", pdf_data))
        if actual_page_count != expected_page_count:
            raise OSError(
                f"El PDF tiene {actual_page_count} páginas; "
                f"se esperaban {expected_page_count}."
            )
        media_boxes = re.findall(rb"/MediaBox\s*\[([^\]]+)\]", pdf_data)
        if len(media_boxes) != expected_page_count or any(
            not re.fullmatch(
                rb"\s*0\s+0\s+612(?:\.0+)?\s+792(?:\.0+)?\s*", media_box
            )
            for media_box in media_boxes
        ):
            raise OSError("El PDF no contiene todas las páginas exactas de 8.5 × 11 in.")
        temporary_path.replace(output_path)
    except BaseException:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise
    finally:
        for image in pdf_images:
            image.close()
    return len(page_images) * 2 - 1


def write_report(
    path: Path,
    continent: str,
    selected_pages: list[tuple[int, int, Path]],
    qa_pages: dict[int, dict[str, object]],
    pdf_page_count: int,
) -> None:
    lines = [
        "Informe de preflight KDP",
        f"Continente: {continent}",
        f"Páginas de historia: {len(selected_pages)}",
        f"Páginas PDF, incluidas las blancas: {pdf_page_count}",
        "Formato: 8.5 × 11 pulgadas, 2550 × 3300 px, 300 DPI",
        "Páginas blancas: una entre cada par de páginas consecutivas",
        "Versiones usadas:",
    ]
    lines.extend(
        f"- Página {page_number}: v{version} — "
        f"{qa_pages[page_number]['status']} — {path.name}"
        for page_number, version, path in selected_pages
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Crea el PDF KDP usando la versión más alta de cada página "
            "aprobada por QA."
        )
    )
    parser.add_argument("--continent", required=True)
    parser.add_argument("--page-count", required=True, type=int)
    parser.add_argument("--qa-manifest", required=True, type=Path)
    parser.add_argument("--pages-root", type=Path, default=Path("pages"))
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.page_count < 1:
        print("Error: el número de páginas debe ser positivo.", file=sys.stderr)
        return 2

    try:
        continent_slug = safe_slug(args.continent)
        pages_directory = args.pages_root / continent_slug
        output_path = args.output or pages_directory / "Bo_KDP_Interior_8.5x11.pdf"
        report_path = output_path.with_name("Bo_KDP_Preflight_Report.txt")
        qa_pages = read_qa_manifest(args.qa_manifest)
        expected_page_numbers = set(range(1, args.page_count + 1))
        if set(qa_pages) != expected_page_numbers:
            raise ValueError(
                "El manifiesto QA no contiene exactamente las páginas "
                f"1–{args.page_count}."
            )
        unplanned_pages = find_unplanned_pages(pages_directory, args.page_count)
        if unplanned_pages:
            raise ValueError(
                f"Hay páginas fuera del plan aprobado: {unplanned_pages}."
            )

        selected_pages: list[tuple[int, int, Path]] = []
        page_images: list[Image.Image] = []
        for page_number in range(1, args.page_count + 1):
            version, page_path = find_latest_page(pages_directory, page_number)
            validate_qa_approval(page_number, version, qa_pages.get(page_number))
            selected_pages.append((page_number, version, page_path))
            page_images.append(inspect_page(page_path))

        pdf_page_count = build_pdf(page_images, output_path)
        write_report(
            report_path, args.continent, selected_pages, qa_pages, pdf_page_count
        )
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"PDF: {output_path.resolve()}")
    print(f"Informe: {report_path.resolve()}")
    print(f"Páginas PDF: {pdf_page_count}")
    for page_number, version, _ in selected_pages:
        print(f"Página {page_number}: v{version} (QA aprobado)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
