---
name: bo-page-compiler
description: Assembles an approved Bo colouring illustration and its exact narrative text into a print-ready portrait page, adding the upper illustration frame, lower text frame, margins and typography. It does not generate or redraw artwork.
---

# Bo Page Compiler

## Mission

Create the **finished printable page** by combining:
1. an approved illustration-only asset from `bo-page-artist`;
2. the matching page row and exact child-facing text from `bo-adventure-storyteller`.

This skill is a layout and typesetting stage. It must not generate, redraw, retouch or creatively alter the illustration. It must not invent or rewrite the story text.

The final page should match the interior-page structure of the supplied Bo book: one framed illustration above and a separate framed text panel below.

## Required inputs

- Approved illustration asset for the current page.
- Matching narrative table row.
- Exact story text for that page.
- Page number and page role.
- Print specification (defaults below).
- Source-book interior PDF or approved layout reference, when available.

If the illustration has not been approved by the user, do not compile it as final. If the exact text is missing, request it rather than reconstructing it.

## Separation of responsibilities

- `bo-page-artist` creates artwork only.
- `bo-page-compiler` creates page layout and typography only.
- `bo-adventure-storyteller` owns the exact story text and narrative content.

Never ask the image-generation model to render the final text or page frames. Use deterministic layout/typesetting tools for the final composition.

## Default print specification

- Trim size: **8.5 × 11 inches**, portrait.
- Recommended production resolution: **300 DPI**.
- Target raster page: **2550 × 3300 px**.
- Background: pure white.
- Interior printing: black ink line art and black text.
- Safe outer margin: at least **0.5 inch** on every side (150 px at 300 DPI).
- No bleed by default.
- Two separate rectangular frames:
  - upper illustration frame: approximately 70% of the usable page height;
  - lower text frame: approximately 25% of the usable page height;
  - remaining usable height: gap and spacing.
- Both frames must align to the same left and right edges.
- Use a clean white gap between the frames.
- Use a thin, consistent black frame stroke similar to the supplied book.

Interpret the 70% / 25% proportions as proportions of the usable interior height after safe margins, not the full trim height. Keep the two frames and gap within the safe area. If exact dimensions from a supplied KDP template or approved layout reference are provided, those dimensions take precedence.

### Default geometry at 300 DPI

For an 8.5 × 11 inch page:
- canvas: 2550 × 3300 px;
- outer safe margin: 150 px;
- usable width: 2250 px;
- usable height: 3000 px;
- frame left/right: x = 150 to 2400 px;
- usable vertical area: y = 150 to 3150 px.

Allocate the usable vertical area approximately as:
- upper illustration frame: 70% = 2100 px;
- inter-frame gap: 5% = 150 px;
- lower text frame: 25% = 750 px.

This is a starting geometry. Adjust the split slightly only when necessary to fit the approved text legibly; preserve the two-frame structure and safe margins. Never allow frames to touch or overlap.

## Illustration placement

- Place the approved artwork inside the upper frame.
- Preserve the artwork's aspect ratio; do not stretch it.
- Fit it inside the frame using a contain/letterbox strategy by default.
- Keep the background white so it blends into the page.
- Do not crop Bo, animals, landmarks or important environmental details.
- If the artwork aspect ratio is unsuitable, ask the artist skill to regenerate at the correct aspect ratio rather than distorting or aggressively cropping it.
- Do not add new objects, textures, shadows or colour.
- Keep the frame line outside the artwork content so it does not cover important outlines.

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
- Large, rounded, friendly children's font in solid black.
- Left aligned.
- Comfortable line spacing and paragraph spacing.
- Sound words should be italicized when indicated by the source text.
- Text must remain fully inside the panel with adequate padding.
- Use a font with full support for the page language and its accents.
- Keep text readable at print size; never solve overflow by shrinking it below a child-friendly readable size.

If the text does not fit:
1. try sensible line wrapping and paragraph spacing adjustments;
2. use a slightly smaller but still legible font within the available panel;
3. if it still does not fit, stop and request an editorially shortened approved text from the user/storyteller. Never silently edit it.

### Exact text rendering
Do not use image generation for lettering. Render text with a deterministic typography/layout engine so that every word and punctuation mark is preserved. Verify the extracted or rendered text against the source string where tooling allows.

## Compilation procedure

1. Confirm that the current illustration is explicitly approved.
2. Confirm that its page number and scene match the narrative row.
3. Load the illustration asset without modifying its content.
4. Create a 2550 × 3300 px white canvas (or the exact user-specified print dimensions at 300 DPI).
5. Draw the upper frame and lower text frame using the geometry above.
6. Fit the illustration inside the upper frame without distortion or loss of important content.
7. Typeset the exact page text inside the lower frame.
8. Export a high-resolution PNG and a print-ready PDF page.
9. Reopen or inspect the output at full resolution.
10. Validate page size, frame positions, margins, text fit, text accuracy and image placement.
11. Present the compiled page for user review.
12. Do not compile the next page until the user approves the current final page.

## Output files

For each page, produce:
- `page_XX_illustration.png` — the approved artwork asset, unchanged;
- `page_XX_final.png` — compiled page at 300 DPI;
- `page_XX_final.pdf` — compiled print-ready PDF page.

Use stable page numbering and filenames. Do not overwrite an already approved final page without explicit user instruction. For revisions, create a clearly identified revision or replace only the current unapproved version.

## Compilation quality gate

- [ ] Illustration was approved by the user.
- [ ] Correct illustration and narrative row are paired.
- [ ] Canvas is 8.5 × 11 inches at 300 DPI (or requested dimensions).
- [ ] Upper illustration frame and lower text frame are present and aligned.
- [ ] Safe margins are respected.
- [ ] Frames have a clean gap and do not overlap.
- [ ] Illustration is not stretched or cropped.
- [ ] No new artwork has been added by the compiler.
- [ ] Exact story text is used, with correct paragraph breaks and italics.
- [ ] Text is legible and contained within the lower frame.
- [ ] No text is placed over the illustration.
- [ ] Final PNG and PDF open correctly and are print-ready.

If any check fails, correct the compilation or return the issue to the artist/storyteller. Never conceal a failed check.

## Human approval and sequencing

After compilation, show the final page and ask:

"Final page [N] is ready for review. Do you approve it?"

If the user requests a change:
- determine whether it concerns the artwork or layout/text;
- route artwork changes to `bo-page-artist`;
- route layout or typography changes to this compiler;
- route story-copy changes to `bo-adventure-storyteller`;
- recompile only after the revised component is approved.

Proceed to the next page only after explicit approval of the final compiled page. Illustration approval alone permits compilation, but does not automatically approve the compiled page.
