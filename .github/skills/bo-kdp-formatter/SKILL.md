---
name: bo-kdp-formatter
description: Assembles quality-approved Bo page PNGs, laid out with the bo-page-compiler prompt, into a KDP interior PDF and preflight report. Defaults to 8.5 × 11 inches; never redesigns or alters page content.
---

# Bo KDP Formatter

## Mission

Take the final PNG pages produced from prompts prepared by `bo-page-compiler` and already passed by `bo-page-quality-auditor`, then assemble them into the final print interior for Amazon Kindle Direct Publishing (KDP).

This skill is a **book-level PDF assembly and preflight stage only**. The `bo-page-compiler` prompt defines the page design; this skill preserves it. It must not:
- generate, redraw, retouch or alter illustrations;
- rewrite, translate, correct or reflow story content in a way that changes wording;
- redesign, add, remove, or resize the page frames or illustration composition;
- silently crop important content;
- repair a failed QA page and then treat it as approved.

Its job is to verify the page PNGs match the approved trim size, set PDF page boxes and print settings without changing page content, apply the approved page order and blank-page strategy, export the PDF, then validate it.

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
4. Confirmation of whether blank reverse sides are required.
5. Final page PNGs matching the approved `bo-page-compiler` template (default: 2550 × 3300 px at 300 DPI).

Optional:
- Requested trim size (width × height and units).
- Bleed requirement.
- Interior ink/paper choice (black-and-white on white paper, black-and-white on cream paper, or colour).
- KDP template or print specification supplied by the user.
- Page count and cover/spine information if the user asks for a full cover wrap (this skill's default scope is interior pages only).

If a required input is missing, ask only for the missing information that materially affects the output. Do not guess whether blank reverse pages are needed.

## Quality gate dependency

Only format pages with status:
- `PASS`, or
- `PASS WITH NOTES` where the user has explicitly accepted the notes.

If a page is `FAIL`, send it back to the responsible skill identified by the QA report. If it is `BLOCKED`, request the missing evidence or file. Never include a failed or blocked page in the final KDP interior.

Before formatting, verify that every supplied page has:
- a unique page identifier;
- an approved final page file;
- a corresponding QA result;
- a known position in the book sequence.

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

Use the narrative/production plan as the authoritative page sequence.

Ask or follow explicit user instructions on whether each illustrated page should have a blank reverse side. If blank backs are required:
- insert one completely blank page after the corresponding printed page;
- ensure blank pages are truly blank (no frame, page number, hidden image, watermark or metadata rendered on the page);
- do not count a blank reverse side as a story/content page in the narrative index;
- update total PDF page count and verify it is compatible with the chosen KDP setup.

Do not add blank pages automatically if the user has not requested them or if the production plan specifies another arrangement.

## Formatting procedure

1. Collect all final pages and QA reports.
2. Reject any page that has not passed QA.
3. Confirm requested trim size; default to 8.5 × 11 inches.
4. Confirm bleed, interior type, paper and blank-page strategy.
5. Inspect each source page's dimensions, orientation and file integrity.
6. Confirm every page was composed using the approved compiler prompt and that the PNG dimensions/effective resolution match the requested page size.
7. Create a consistent PDF with the exact target physical page size.
8. Embed each approved page at native size, without resizing, cropping, padding or changing its layout.
9. Insert blank reverse pages only when requested.
10. Assemble pages in the approved order.
11. Export a print-ready interior PDF.
12. Reopen the PDF and inspect page count, page dimensions, orientation, page order, blank pages and rendering.
13. Produce a concise KDP preflight report.

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
- [ ] Blank reverse pages included only as requested.
- [ ] Blank pages are actually blank.
- [ ] No accidental duplicate, missing or out-of-order pages.
- [ ] PDF assembly has not changed the approved page design.

If any check fails, do not label the PDF KDP-ready. Explain the failure and route it to the responsible upstream skill or request the missing KDP settings.

## Required final report

Return:

### KDP interior formatting report
- Requested trim size:
- Actual PDF page size:
- Orientation:
- Page count:
- Blank reverse pages:
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

Its deliverable is a correctly sized, consistently assembled, preflight-checked interior PDF. Per-page frames and typography are created from prompts prepared by `bo-page-compiler`; this formatter only assembles and validates those final pages.
