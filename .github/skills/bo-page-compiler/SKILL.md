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
- Match the Japan sample page: approximately **0.48 inch** outer margins at the sides, **0.20 inch** at the top, and **0.19 inch** at the bottom.
- No bleed by default.
- Two separate rectangular frames:
  - both frames approximately **7.55 inches wide**, centered and aligned;
  - upper illustration frame approximately **8.00 inches high**;
  - lower text frame approximately **2.50 inches high**;
  - white gap approximately **0.12 inch**.
- Rounded corners, matching between frames; uniform black outline approximately 2–2.5 pt at print size.

These dimensions are measured from the Japan sample's illustration frame and text frame and fit the 8.5 × 11 inch canvas. Do not combine incompatible percentages or let frames exceed the canvas. If the user supplies an approved reference template, follow it while preserving the exact requested page size.

### Default geometry at 300 DPI

For the default 8.5 × 11 inch page, the prompt should specify a 2550 × 3300 px portrait canvas, with this measured sample geometry:
- centered frame width: 2264 px (about 7.55 inches);
- upper illustration frame height: 2399 px (about 8.00 inches);
- gap: 35 px (about 0.12 inch);
- lower text frame height: 749 px (about 2.50 inches);
- horizontal side margins: about 143 px (0.48 inch);
- top margin: about 61 px (0.20 inch); bottom margin: about 56 px (0.19 inch).

Keep both frames inside the canvas, with equal widths and a consistent gap. These measurements take precedence over percentage descriptions if those would conflict.

## Illustration placement

- Place the approved artwork inside the upper frame.
- Every approved illustration uses the same 1024 × 1085 px canvas, matching the Japan sample's upper-frame ratio (about 0.944:1). Place it centered in the upper frame with aspect-ratio-preserving containment; do not stretch, crop, or distort it. The ratios are nearly identical.
- Preserve the original background and line art.
- Maximize visible image size with a minimal, even inset of approximately 0.05 inch.
- Do not stretch, distort, crop, redraw, regenerate, retouch, recolour, add to or remove anything.
- If it cannot fit without cropping or distortion, stop and request a correctly proportioned approved illustration.

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
- Large, rounded, friendly children's font in solid black, centered horizontally.
- Target 15–17 pt at 300 DPI, with comfortable 1.3–1.4 line spacing and paragraph spacing.
- Sound words should be italicized when indicated by the source text.
- Text must remain fully inside the panel with adequate padding.
- Use a font with full support for the page language and its accents.
- Use the largest size that fits legibly; never omit, rewrite or shrink excessively to conceal overflow.

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

PLANTILLA FIJA: Usa exactamente dos marcos rectangulares independientes, centrados, con esquinas redondeadas idénticas y el mismo ancho. Traza bordes negros finos y uniformes de aproximadamente 2–2,5 pt a tamaño de impresión. Usa la geometría medida de la página de referencia de Japón: marcos de aproximadamente 7,55 pulgadas (2264 px) de ancho; marco superior de ilustración de aproximadamente 8,00 pulgadas (2399 px) de alto; marco inferior de texto de aproximadamente 2,50 pulgadas (749 px) de alto; separación blanca de aproximadamente 0,12 pulgadas (35 px); márgenes laterales de 0,48 pulgadas (143 px), margen superior de 0,20 pulgadas (61 px) e inferior de 0,19 pulgadas (56 px). Mantén toda la geometría dentro del lienzo de 2550 × 3300 px. No añadas ningún otro marco, borde ni elemento de maquetación.

MARCO SUPERIOR — ILUSTRACIÓN APROBADA: Usa la ilustración adjunta como arte definitivo. Su proporción es 1024 × 1085 px, medida para coincidir con el marco de ilustración de la página de referencia de Japón (no con su panel de texto). Colócala dentro del marco superior conservando su proporción y todos sus detalles. No la estires, deformes, recortes, redibujes, regeneres, retoques, recolorees, ni añadas o elimines elementos. Maximiza el tamaño visible sin recortar nada. Si no es posible, detente en lugar de alterar la ilustración.

MARCO INFERIOR — TEXTO EXACTO: Incluye únicamente el texto siguiente, conservando exactamente cada palabra, acento, signo de puntuación, diálogo y salto de párrafo. No añadas título, número de página, subtítulo, explicación ni ningún otro texto. Céntralo horizontalmente con una tipografía infantil redondeada y muy legible, en negro; idealmente de 15–17 pt a 300 DPI, con interlineado aproximado de 1,3–1,4 y separación cómoda entre párrafos. Usa el tamaño más grande que quepa. No reescribas ni omitas texto para que quepa; si no cabe de forma legible, detente y solicita una versión aprobada más breve.

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
- [ ] Prompt requires exactly two matching frames and the Japan sample's measured dimensions, gap and margins.
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
