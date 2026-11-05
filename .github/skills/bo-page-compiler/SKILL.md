---
name: bo-page-compiler
description: Creates complete page-layout prompts with exact story text and approved illustrations for final-page-ia. Supports compiling all eligible pages in a requested batch without intermediate approvals.
---

# Bo Page Compiler

## Mission

Create a **complete, page-specific prompt and API handoff** combining:
1. an approved illustration-only asset from `bo-page-artist`;
2. the matching page row and exact child-facing text from `bo-adventure-storyteller`.

`final-page-ia` sends the exact prompt and identified approved illustration file to the OpenAI Images API to produce the finished page. This skill prepares the prompt and identifies the image path; it does not itself generate or export the finished page.

The prompt must describe one consistent interior-page template: one framed illustration above and a separate framed text panel below.
Write the prompt in the user's language (Spanish by default), while preserving the approved page text exactly in its source language.

## Required inputs

- Approved illustration asset for the current page.
- Exact repository path of that approved illustration, including its version directory.
- Matching narrative table row.
- Exact story text for that page.
- Page number and page role.
- Print specification (defaults below).
- Approved layout reference, when available.

If the illustration has not been approved by the user, do not compile it as final. If the exact text is missing, request it rather than reconstructing it.

## Separation of responsibilities

- `bo-page-artist` creates artwork only.
- `bo-page-compiler` creates the prompt with exact page text and identifies the precise illustration file; it does not create the page image.
- `final-page-ia` uploads that precise illustration and the compiler prompt to the image API and saves the finished page.
- `bo-adventure-storyteller` owns the exact story text and narrative content.
- `bo-kdp-formatter` assembles the latest QA-approved page PNG versions into the book's print-ready PDF.

Make the prompt explicit that the supplied illustration is final and must be placed, not regenerated, and that all supplied page text must be rendered exactly. Do not claim that a prompt guarantees exact text or print metadata: the returned page must pass the quality audit and technical preflight before it is treated as print-ready.

## Default print specification

- Trim size: **8.5 × 11 inches**, portrait.
- Recommended production resolution: **300 DPI**.
- Target raster page: **2550 × 3300 px**.
- Every completed page must use exactly this same 2550 × 3300 px canvas so all pages fit the 8.5 × 11 inch KDP interior.
- Background: pure white.
- Interior printing: black ink line art and black text.
- Keep at least **0.25 inch** at the outer edge and the KDP-required inside/gutter margin (at least **0.375 inch** for a short book); mirror the inside margin for verso and recto pages. Use **0.20 inch** at the top and **0.19 inch** at the bottom unless the print specification requires more.
- No bleed by default.
- Two separate rectangular frames:
  - both frames use the maximum width allowed by the safe margins; for 0.375-inch inside and 0.25-inch outside margins, this is **7.875 inches** (about **2362 px**), aligned within the safe area and mirrored for verso/recto pages;
  - upper illustration frame follows the approved art's aspect ratio. For the standard 1024 × 1085 px illustration, it is about **7.875 × 8.34 inches** (2362 × 2502 px);
  - the lower text frame uses only the height needed for the exact text, up to the remaining safe area (about **2.15 inches / 645 px** with the standard geometry);
  - white gap approximately **0.12 inch**.
- Rounded corners, matching between frames; uniform black outline approximately 2–2.5 pt at print size.

The illustration is the primary content and must occupy at least **70% of the full 8.5 × 11-inch page area**, with a preferred target around **75% where the approved art's aspect ratio and print-safe margins permit**. Calculate this from the placed rectangle of the approved illustration (its full image footprint, including its original white background), divided by 2550 × 3300 px; do not count extra blank frame space or added padding. Do not combine incompatible dimensions, let frames exceed the canvas, or reduce required KDP margins to reach the target. For the standard 1024 × 1085 px art and 0.375/0.25-inch side margins, maximum undistorted artwork occupies about **70.2%** of the page; this is the practical limit for that aspect ratio. If the required gutter or the approved art's aspect ratio makes 70% impossible, flag the layout as blocked and request an approved layout/artwork change instead of cropping or distorting the art.

### Default geometry at 300 DPI

For the default 8.5 × 11 inch page and 1024 × 1085 px approved art, specify:
- canvas: 2550 × 3300 px;
- both frame widths: about 2362 px (7.875 inches), with inside/outside margins mirrored for verso/recto;
- upper illustration frame: about 2362 × 2502 px (7.875 × 8.34 inches), matching the approved art's ratio;
- placed illustration footprint: about 5,910,000 px, or **70.2%** of the full page;
- gap: about 36 px (0.12 inch);
- maximum lower text frame height: about 645 px (2.15 inches), including its border;
- top margin: about 60 px (0.20 inch); bottom margin: about 57 px (0.19 inch).

Keep both frames inside the canvas and use the exact approved art ratio. Recalculate width from the actual KDP gutter/outer-margin requirement and height from the art ratio; do not reuse these pixel dimensions blindly for different page counts, margins, or artwork ratios.

## Illustration placement

- Place the approved artwork inside the upper frame.
- Standard approved illustrations use a 1024 × 1085 px canvas (about 0.944:1). Place the entire artwork at the largest size that fits the safe frame with its aspect ratio preserved. Do not stretch, crop, distort, or add blank padding outside the approved image.
- Preserve the original background and line art.
- Maximize visible image size within the print-safe frame; keep only a minimal inset needed to prevent the art touching the border.
- Do not stretch, distort, crop, redraw, regenerate, retouch, recolour, add to or remove anything.
- If the placed image footprint cannot reach 70% of the page without cropping, distortion, or unsafe margins, stop and request an approved layout/artwork change.

## Text typesetting

The narrative table is authoritative. Copy the exact text, including:
- spelling and capitalization;
- punctuation;
- accents and diacritics;
- apostrophes and quotation marks;
- paragraph breaks;
- italics indicated for sound words.

Do not paraphrase, translate, correct, shorten, expand or add any words.

### Text panel
- Plain white background.
- Separate rectangular frame.
- No illustration, decorative graphics or watermark behind the words.
- Match the lettering in the approved visual reference [pages/africa/page_6.v3.png](../../../pages/africa/page_6.v3.png): a rounded, handwritten-looking sans serif with thick black strokes, smooth curves and simple lowercase forms. The exact font is unknown; reproduce its appearance consistently rather than claiming a font name.
- The six-printed-line reference has an approximately **2362 × 954 px** lower frame and a visible text block of **1780 × 835 px**, centered at about 75% of frame width and 87% of frame height, with roughly **290 px** side padding and **60 px** top/bottom padding. These are measurements of the reference only: they cannot be used as fixed dimensions alongside the minimum 70% illustration-area requirement.
- The standard illustration leaves at most about **645 px** for the lower frame, including its border, at the default 8.5 × 11-inch trim and safe margins. Calculate the actual remaining safe space for each page and size both the panel and text block to fit within it; the text frame must never force the illustration below 70% of the page. Center the text block horizontally and vertically in its panel.
- Treat the reference's **120 px** line pitch, **1–3 px** within-paragraph contour gaps, **70 px** before “Stamp!”, and **46 px** before the final paragraph as visual starting points, not hard constraints. The font family/style, regular/bold weights, and apparent character height are a book-wide design system: keep them virtually identical across pages. First use the available text width and sensible wrapping; then make only minimal reductions to paragraph gaps and line pitch to fit the actual wrapped line count. Do not redesign individual pages' typography to make room for the illustration.
- Set **“Stamp!”** in bold without making it larger than the surrounding text. Keep other text in the regular weight.
- Destination copy has three semantic lines (place, stamp, animal clue), which may wrap. Do not force six printed lines or add text to fill the reference block. Preserve the reference's typeface appearance and proportions as closely as possible within the space available. Keep apparent character height at the reference size whenever possible; if absolutely necessary, reduce it by no more than **5%** and use that same size consistently across all pages in the book, not just the crowded page. First adjust line wrapping, then reduce paragraph gaps and line pitch slightly (no more than **5%** from the reference). If the exact text still cannot fit legibly within these small adjustments while preserving the 70% illustration minimum and print-safe margins, stop and request an approved shorter text; never shrink the illustration below the minimum or make a larger typography change on a single page.
- Sound words should be italicized when indicated by the source text.
- Text must remain fully inside the panel with adequate padding.
- Use a font with full support for the page language and its accents.
- Keep typeface, apparent letter height, weight and line pitch virtually identical across pages. Any necessary scale/spacing adjustment is limited to 5%, applied consistently to the whole book, and must not be used to conceal overflow. Do not infer a point size from the PNG.
- Size the text panel to the exact approved text, using the remaining safe vertical area after the illustration and gap. A shorter text may use a shorter panel; it must not cause the illustration to be reduced below its 70% page-area minimum.

If the text does not fit:
1. try sensible line wrapping and paragraph spacing adjustments;
2. if it still does not fit legibly, stop and request an editorially shortened approved text from the user/storyteller. Never silently edit it.

### Exact text rendering
The prompt must emphasize that every word and punctuation mark is authoritative and exact. Treat the returned image as unverified until its text has been checked against the source.

## Procedure

1. Confirm the current illustration is explicitly approved, matches the narrative row, and its exact repository path and version are known.
2. Confirm the exact approved child-facing text and the page number/role. Do not invent missing information.
3. If an input is missing, mismatched or ambiguous, ask for it rather than reconstructing it in single-page mode. In batch mode, mark that page blocked, continue with the other eligible pages, and report the blocked page with the batch instead of pausing to ask.
4. Fill every part of the prompt template below with page-specific details and the exact complete text. Do not leave placeholders or omit story text.
5. Return the complete prompt in one code block and a separate handoff record containing the exact illustration path, continent, page number and approved source text. Never say "latest illustration" without giving the exact file path.
6. Pass the prompt and handoff record to `final-page-ia`. It uploads precisely that illustration path, not another version or an image inferred from the page number.
7. Check the returned page against the template and exact source text. If any element fails or cannot be verified, explain the issue and request a correction prompt; do not call it print-ready.
8. Pass the exact saved page version to `bo-page-quality-auditor`. Only auditor-approved versions proceed to `bo-kdp-formatter`.
9. In single-page mode, wait for the user's explicit approval of the current final page before moving to the next page. In an explicitly requested batch covering all pages in a defined plan, compile every eligible page without per-page approval pauses; maintain exact page-to-illustration and page-to-text matching, and collect the handoffs for the complete batch before returning them to `final-page-ia`.

## Batch layout mode

- Activate batch mode only when the user explicitly asks to lay out all pages or generate the complete set of finished pages at once, and the story plan defines the batch scope.
- Use only illustrations already approved for layout, and only the exact page text and illustration paths specified by the plan. Do not skip a page silently; if its approved illustration or text is missing, mark that page blocked and continue preparing the other eligible pages.
- Prepare an independent, complete prompt and exact handoff record for each page. Never combine multiple page illustrations or texts into a single page-generation request.
- Return the batch handoffs together. Do not ask for approval after compiling each page, between handoffs, or before proceeding to the next eligible page. Do not pause the batch to request missing inputs; record the affected page as blocked and report it with the completed batch.

## Copy-ready prompt template

Maqueta una página interior completa para un libro infantil para colorear. La API recibirá como imagen de referencia el archivo exacto indicado en la entrega del compiler. Usa ese archivo como ilustración terminada y aprobada; tu tarea es exclusivamente maquetarla.

FORMATO DE SALIDA: Devuelve exactamente una página PNG vertical de 2550 × 3300 píxeles y 300 DPI, equivalente a 8,5 × 11 pulgadas. Usa fondo blanco puro (#FFFFFF) y sin sangrado. No devuelvas una maqueta, descripción, alternativas ni páginas adicionales.

PLANTILLA DE IMPRESIÓN: Devuelve una página de 2550 × 3300 px (8,5 × 11 pulgadas, 300 DPI), fondo blanco y sin sangrado. Usa exactamente dos marcos rectangulares independientes, con esquinas redondeadas idénticas y del mismo ancho, alineados dentro del área segura de impresión (no necesariamente centrados respecto a todo el lienzo); refleja la posición para páginas pares e impares. Ajusta el ancho máximo a los márgenes KDP necesarios para el grosor final del libro: al menos 0,25 pulgadas en el borde exterior y el margen interior requerido (al menos 0,375 pulgadas para un libro corto). Para la ilustración adjunta de 1024 × 1085 px, usa el mayor tamaño que cabe sin recortar ni deformar; con esos márgenes, el marco superior mide aproximadamente 2362 × 2502 px (7,875 × 8,34 pulgadas), y la huella rectangular de la ilustración ocupa alrededor del 70,2% del área total de página. Cuenta el rectángulo de la imagen aprobada completa (incluido su fondo blanco original), no el espacio vacío añadido entre la imagen y el marco. Deja una separación blanca aproximada de 36 px (0,12 pulgadas), margen superior de unos 60 px (0,20 pulgadas) e inferior de unos 57 px (0,19 pulgadas). Ajusta el marco inferior al texto exacto y al espacio seguro restante (máximo aproximado 645 px / 2,15 pulgadas con esta geometría). Si el margen interior requerido es mayor, recalcula las dimensiones y comprueba que la huella de la imagen aprobada siga ocupando al menos el 70% de toda la página; si no es posible, detente e informa del conflicto. No añadas ningún otro marco ni elemento de maquetación.

MARCO SUPERIOR — ILUSTRACIÓN APROBADA: Usa la ilustración adjunta como arte definitivo y colócala completa dentro del marco, conservando su proporción y todos sus detalles. No la estires, deformes, recortes, redibujes, regeneres, retoques, recolorees, ni añadas o elimines elementos. Maximiza el tamaño del archivo de imagen completo dentro de los márgenes de impresión. El objetivo es que la huella rectangular de la imagen ocupe entre el 70% y el 75% de toda la página siempre que lo permitan su proporción y los márgenes seguros; nunca menos del 70%. El fondo blanco que ya forma parte del archivo aprobado cuenta dentro de su huella; no añadas espacio en blanco entre la imagen y el marco. Si no es posible cumplir el mínimo, detente en lugar de alterar la imagen o invadir los márgenes.

MARCO INFERIOR — TEXTO EXACTO: Incluye únicamente el texto siguiente, conservando exactamente cada palabra, acento, signo de puntuación y salto de párrafo. No añadas título, número de página, subtítulo, explicación ni ningún otro texto. Imita la referencia visual pages/africa/page_6.v3.png: sans serif redondeada de aspecto manuscrito, trazos negros gruesos y curvas suaves. Centra el bloque completo en el panel. Las medidas de la referencia de seis líneas (marco de 2362 × 954 px, bloque visible de 1780 × 835 px, paso vertical de 120 px y sus separaciones entre párrafos) son solo una guía visual; no las impongas como dimensiones, pues la ilustración debe conservar al menos el 70% del área total de página. En esta plantilla, el panel inferior suele tener como máximo unos 645 px de alto. Calcula el espacio restante real después de colocar la ilustración y ajusta a él el panel y el bloque de texto. Mantén en todas las páginas la misma fuente de aspecto, peso y altura aparente de letra de la referencia; deben verse prácticamente iguales. Primero utiliza el ancho seguro disponible y ajusta el salto de línea; si hace falta, reduce los espacios entre párrafos y el paso vertical solo un poco, hasta un 5%. Reduce la altura aparente de letra como último recurso y nunca más de un 5%; cualquier cambio de tamaño se aplica de forma uniforme a todas las páginas, no solo a esta. Escribe “Stamp!” en negrita sin hacerlo más grande que las demás letras. No fuerces seis líneas impresas ni añadas texto para llenar espacio. Nunca reduzcas la ilustración por debajo del 70%, invadas márgenes ni recortes el texto. Si el texto exacto no cabe de manera legible con estos ajustes mínimos, detente y solicita una versión aprobada más breve; no cambies notablemente la tipografía de esta página.

<TEXTO_DE_LA_PAGINA>
[Inserta el texto completo aprobado para esta página, respetando los saltos de párrafo.]
</TEXTO_DE_LA_PAGINA>

NO HAGAS LO SIGUIENTE: crear o modificar la ilustración; recortarla o deformarla; cambiar su fondo o sus trazos; añadir mapas, objetos, adornos, sombras, color, grises, etiquetas, marcas de agua, firmas ni texto adicional; permitir que los marcos o el texto se recorten o se superpongan.

Antes de devolver la página, comprueba las dimensiones exactas, los dos marcos, los márgenes, la alineación, la separación, la conservación de la imagen, la integridad del texto y su legibilidad. Devuelve únicamente el PNG.

Sustituye el marcador de texto por el texto exacto aprobado antes de presentar el prompt. Incluye únicamente el texto de esta página. Fuera del bloque del prompt, incluye una ficha de entrega: continente; número de página; ruta relativa exacta de la ilustración aprobada (incluido `vN`); texto aprobado exacto utilizado.

## Prompt handoff quality gate

- [ ] Correct approved illustration, exact versioned repository path and matching narrative row are available.
- [ ] Prompt includes the complete exact source text and preserves its paragraph breaks.
- [ ] Prompt specifies the fixed 8.5 × 11 inch, 2550 × 3300 px, 300 DPI template.
- [ ] Prompt requires the placed rectangle of the complete approved illustration to occupy at least 70% of the full page area, preferably about 75% where the approved aspect ratio and safe margins allow.
- [ ] Prompt uses 8.5 × 11-inch KDP-safe geometry recalculated for the final gutter and exact approved art ratio, not the old Japan sample dimensions.
- [ ] Prompt matches the lettering in `pages/africa/page_6.v3.png`; treats its six-line pixel dimensions as references only; fits the panel and text block to the actual safe space while keeping the illustration at or above 70%; keeps typography virtually identical across pages (maximum 5% adjustment, applied consistently book-wide); and sets “Stamp!” bold without enlarging it.
- [ ] Prompt prohibits image alteration, text changes and extra elements.
- [ ] Prompt is complete, page-specific, in the user's language, with all approved text in one copy-ready block and no unresolved placeholders.
- [ ] Handoff identifies the exact illustration filepath, including the version directory, for `final-page-ia`.
- [ ] No claim is made that the resulting page has already been generated or technically verified.

## Review and sequencing

For a single-page request, after the user returns a page, ask:

"La página maquetada [N] está lista para revisión. ¿La apruebas?"

If the user requests a change:
- determine whether it concerns the artwork, layout or text;
- route artwork changes to `bo-page-artist`;
- provide a targeted prompt revision for layout or typography changes;
- route story-copy changes to `bo-adventure-storyteller`;
- rebuild the prompt with revised, approved inputs.

For a single-page request, proceed to the next page only after explicit approval of the final composed page. Illustration approval alone does not approve the composed page.

For an explicitly requested full-page batch (for example, «haz todas las páginas» or «genera el libro completo»), do not stop for approval between pages or wait for approval of an individual composed page before continuing. After every eligible page has been composed and quality-audited, present the complete batch and its page-by-page audit results together and request one approval for the set. Do not send pages with a failed or blocked audit to `bo-kdp-formatter`. A batch request waives intermediate approval pauses only; it does not waive illustration approval, text accuracy, QA, or the user's final approval of the batch for print production.
