---
name: bo-kdp-formatter
description: After bo-page-quality-auditor approves every final page, selects the highest version of each page in pages/<continent>/, inserts one blank page between consecutive pages, and assembles the KDP interior PDF.
---

# Bo KDP Formatter

## Mission

After every expected page has passed `bo-page-quality-auditor` and received user approval, find the highest numbered saved version of each page in `pages/<continent>/`, then assemble those pages into the final print interior for Amazon Kindle Direct Publishing (KDP). Insert exactly one blank white page between each pair of consecutive story pages; do not append an extra blank page after the last story page.

This skill is a **book-level PDF assembly and preflight stage only**. The `bo-page-compiler` prompt defines the page design; this skill preserves it. It must not:
- generate, redraw, retouch or alter illustrations;
- rewrite, translate, correct or reflow story content in a way that changes wording;
- redesign, add, remove, or resize the page frames or illustration composition;
- silently crop important content;
- repair a failed QA page and then treat it as approved.

Its job is to enforce complete QA approval for the latest version of every expected page, preserve the page content, insert the required interleaved blank pages, export the PDF, then validate page count, order, dimensions and blanks.

Do not treat PDF assembly as a substitute for the per-page layout prompt. Do not create a competing page template here; use the same fixed design as `bo-page-compiler`.

## Default format

Unless the user explicitly requests another size, use:

- **Trim size: exactly 8.5 × 11 inches**
- Orientation: portrait
- PDF page size: exactly 612 × 792 points (8.5 × 11 inches)
- Raster artwork target: 300 DPI where raster assets are used
- Equivalent raster canvas: 2550 × 3300 pixels at 300 DPI
- Interior: black-and-white unless the user explicitly requests another print interior type
- Bleed: **no bleed by default**, unless the approved design/KDP setup explicitly requires bleed
- Keep all content within the approved page design and KDP's applicable requirements. The page's white outer margin and frame dimensions come from the approved `bo-page-compiler` template; do not silently resize the design to meet a different margin assumption.

"Exactly 8.5 × 11 inches" means the PDF MediaBox/CropBox page dimensions must be 612 × 792 points (subject only to normal PDF floating-point precision). Do not rely only on the file name, metadata label or pixel dimensions.

## Inputs

Required:
1. Final page files that have passed `bo-page-quality-auditor`.
2. QA report/status for every page.
3. Page order from the approved narrative/production plan.
4. Expected page count and sequence from the approved production plan.
5. QA manifest/report that explicitly approves the exact latest version of every page. Required JSON shape:
   `{"pages":{"1":{"status":"PASS","version":2},"2":{"status":"PASS WITH NOTES","version":1,"user_accepted_notes":true}}}`
6. Final page PNG versions in `pages/<continente>/page_<n>.v<m>.png`, produced by `final-page-ia`.

Optional:
- Requested trim size (width × height and units).
- Bleed requirement.
- Interior ink/paper choice (black-and-white on white paper, black-and-white on cream paper, or colour).
- KDP template or print specification supplied by the user.
- Page count and cover/spine information if the user asks for a full cover wrap (this skill's default scope is interior pages only).

If the page count, sequence, QA results, or a latest page version is missing or ambiguous, ask for it and do not produce a partial book.

## Quality gate dependency

Only format pages with status:
- `PASS`, or
- `PASS WITH NOTES` where the user has explicitly accepted the notes.

If a page is `FAIL`, send it back to the responsible skill identified by the QA report. If it is `BLOCKED`, request the missing evidence or file. Never include a failed or blocked page in the final KDP interior.

Before formatting, verify that every expected page has:
- a unique page identifier;
- an approved final page file;
- a corresponding `PASS` QA result for the exact highest version on disk, or `PASS WITH NOTES` with explicit user acceptance for that exact version;
- a known position in the book sequence.

The QA manifest must include the page number, QA status and approved version for every expected page. The selected file version must equal the version listed in the manifest. If a newer correction exists without a fresh passing audit, stop; do not silently fall back to an older passing version. Do not omit missing pages or build a partial PDF.

## KDP specification handling

KDP print requirements can depend on trim size, page count, paper, ink, bleed and binding.

- Use the user's explicit KDP template/specification when supplied.
- If current KDP rules need to be confirmed and web access is available, consult official Amazon KDP help/documentation only.
- Do not invent minimum margins, gutter values, bleed allowances, page-count limits or cover-spine dimensions.
- If the required KDP specification cannot be verified, clearly state what remains unverified and request the relevant KDP template/settings. In particular, do not claim a margin is KDP-compliant solely because it matches the page-layout prompt.
- This skill formats the **interior** by default. Do not calculate or create a full cover wrap unless explicitly requested and all required page-count, paper and bleed inputs are known.

For a no-bleed interior, verify the approved page meets the selected safe-area requirements. If it does not, return it for a revised page-layout prompt and regenerated page; do not shrink, crop, reposition or otherwise alter the approved page to force compliance. For bleed, use the exact KDP bleed dimensions for the chosen trim size and have the page layout recreated to that specification; do not scale the no-bleed page.

## Page geometry and scaling

### Default 8.5 × 11 inches

- Target PDF page: 612 × 792 pt.
- Target raster page: 2550 × 3300 px at 300 DPI.
- Portrait orientation.
- No accidental rotation.

### Other requested formats

If the user requests another trim size:
1. Parse width, height and units.
2. Convert to points and inches.
3. Confirm orientation.
4. Use the exact requested physical dimensions for every PDF page.
5. Verify the approved page-layout prompt and regenerated PNGs use dimensions and safe areas suitable for that trim size.
6. Preserve aspect ratios; never stretch artwork or text.
7. If the new format makes the existing approved design unsuitable, stop and explain the issue. Request a layout revision from `bo-page-compiler` rather than cropping important content or distorting the page.

### Scaling rules

- For the default 8.5 × 11 inch interior, place each 2550 × 3300 px page PNG on an 8.5 × 11 inch PDF page at its native size, without resizing or modifying pixels.
- Verify that the PNG dimensions and effective resolution support the exact target page size. If they do not, return the page to `bo-page-compiler` for a revised prompt and regenerated page.
- For another trim size or bleed setting, request page assets composed to that specification through `bo-page-compiler`; do not scale, crop or pad an already approved page.
- Never stretch an illustration or finished page non-uniformly.
- Never crop Bo, landmarks, text, frames or any meaningful content.
- Do not add or remove frames; do not alter the approved design.
- Do not change the exact approved text.

## Page order and blank reverse sides

Use the approved production plan as the authoritative sequence and expected page count. Always insert exactly one completely blank page between every pair of consecutive final story pages. A book with N final pages therefore has `2N - 1` PDF pages. Do not add a blank page before the first or after the last story page. Blank pages contain no frame, page number, hidden image, watermark or rendered metadata. Do not count blank pages as story pages.

For each expected page number, select the highest existing filename version `page_<n>.v<m>.png` under `pages/<continent>/`. Include exactly one final page per story page, in ascending page-number order. Do not include lower versions, unplanned page numbers, duplicate pages or a page whose selected version lacks a passing QA result.

Run the formatter script after receiving the manifest:

```powershell
python .github\skills\bo-kdp-formatter\scripts\format_interior.py `
  --continent "<continente>" `
  --page-count <cantidad-de-paginas> `
  --qa-manifest "<ruta-al-manifiesto-qa.json>"
```

The script selects the highest version on disk, requires that same version to be audited, checks the 2550 × 3300 px / 300 DPI page files, and writes the PDF and report under `pages/<continente>/`. Do not run it before all page approvals are present.

## Formatting procedure

1. Read the expected page count/order and QA manifest after all pages have been audited and approved.
2. Discover the highest `vN` file for each expected page in `pages/<continent>/`.
3. Confirm that the QA manifest approves that exact highest version for every page. Stop if a status is FAIL/BLOCKED, a page/version is missing, or a newer version is unaudited.
4. Confirm requested trim size; default to 8.5 × 11 inches.
5. Confirm bleed and interior type/paper settings. The blank-between-pages rule is mandatory and is not optional.
6. Inspect each selected source page's dimensions, orientation, DPI metadata and file integrity.
7. Create a PDF with the exact target physical page size and place each approved 2550 × 3300 px PNG at native 300-DPI size, without resizing, cropping or changing its layout.
8. Add exactly one pure-white blank PDF page between consecutive story pages, with no trailing blank.
9. Assemble in ascending page order and save `Bo_KDP_Interior_8.5x11.pdf` under `pages/<continent>/` (or reflect a requested trim size in the name).
10. Reopen or parse the PDF and verify its dimensions, page count (`2N - 1`), page order, each interleaved blank page and successful rendering.
11. Produce a concise preflight report listing the exact selected page versions and their QA status.

## Output files

By default, produce:
- `Bo_KDP_Interior_8.5x11.pdf` — final print interior.
- `Bo_KDP_Preflight_Report.txt` — formatting checks, dimensions, page count, bleed and any unresolved KDP settings.

For a different requested size, reflect it in the filename, for example:
- `Bo_KDP_Interior_8x10.pdf`

Keep source page files unchanged. Do not overwrite the approved source pages.

## KDP preflight checks

### Document dimensions
- [ ] Every PDF page has the exact requested trim size.
- [ ] Default is exactly 8.5 × 11 inches (612 × 792 pt) unless overridden.
- [ ] All pages have consistent orientation and dimensions.
- [ ] No unintended rotation or mixed-size pages.
- [ ] Each page PNG matches the approved compiler layout and is embedded at native size.

### Content and safe area
- [ ] All pages have passed QA.
- [ ] Page sequence matches the approved plan.
- [ ] No content is stretched or distorted.
- [ ] No important content is cropped.
- [ ] Safe margins comply with the applicable KDP specification.
- [ ] Bleed is correctly applied or explicitly set to none.
- [ ] No unintended marks or content appear outside the trim area.

### Print quality
- [ ] Raster assets have adequate effective resolution for the output size (target 300 DPI).
- [ ] Black-and-white pages remain black and white.
- [ ] No unexpected colour conversion, transparency artefacts or grey backgrounds have appeared.
- [ ] Frames and text remain crisp and legible.
- [ ] Fonts are embedded or otherwise rendered reliably in the PDF.
- [ ] PDF opens and renders correctly.

### Book structure
- [ ] Correct page count.
- [ ] Exactly one blank page appears between every pair of story pages, with none before the first or after the last.
- [ ] Total PDF page count is `2N - 1` for N story pages.
- [ ] Blank pages are actually blank.
- [ ] No accidental duplicate, missing or out-of-order pages.
- [ ] PDF assembly has not changed the approved page design.
- [ ] The highest on-disk version of every page is the version approved in the QA manifest.

If any check fails, do not label the PDF KDP-ready. Explain the failure and route it to the responsible upstream skill or request the missing KDP settings.

## Required final report

Return:

### KDP interior formatting report
- Requested trim size:
- Actual PDF page size:
- Orientation:
- Page count:
- Blank reverse pages:
- Selected highest page versions and QA status:
- Bleed:
- Interior type / paper:
- Effective raster resolution:
- QA status of included pages:
- KDP specification source or assumptions:

### Preflight result
`READY FOR KDP UPLOAD` / `NOT READY`

List all failed checks and unresolved assumptions. Do not claim Amazon will accept the file; state only that it passed the checks performed against the selected specification.

## Boundaries

This skill does not:
- create a cover or calculate spine width unless explicitly commissioned;
- upload or publish the book to KDP;
- guarantee KDP acceptance;
- change the content to fix layout problems;
- bypass the QA gate.

Its deliverable is a correctly sized, consistently assembled, preflight-checked interior PDF with one blank page between consecutive pages. It runs only after every latest page version has passed the auditor and received the required approval.
