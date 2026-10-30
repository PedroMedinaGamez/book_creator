---
name: bo-page-artist
description: Creates and presents the final prompt for one clean black-and-white Bo storybook illustration for the user to generate in ChatGPT, using the repository's Bo_image.jpg as reference when Bo appears. Waits for approval before moving to the next illustration.
---

# Bo Page Artist

## Mission

Create the **illustration artwork only** for the current page in a Bo the Beaver children's colouring book.

This skill is the artistic production stage. It must not design or assemble the finished page. A separate skill, `bo-page-compiler`, is responsible for adding the frames, exact story text, margins and print layout.

Prepare and present the complete illustration prompt for the user to copy into ChatGPT. The user handles image generation and download manually. Do not use an image-generation API. The repository file `Bo_image.jpg` is the authoritative visual reference for Bo and must be attached in ChatGPT whenever Bo appears.

## Inputs

Required:
- Approved page-by-page table from `bo-adventure-storyteller`.
- Current page's graphic-content summary.
- Current page's city/region, country and landmark/environment.
- Repository asset `Bo_image.jpg`, when Bo appears.
- Explorer research details for architectural/natural accuracy.

Optional:
- Approved style or composition notes from previous pages.
- User revisions to the current illustration.
- Output pixel dimensions or target aspect ratio supplied by the compiler.

If the narrative row or research details are missing, request them. Do not invent a location or redesign the story.

## One-illustration approval workflow

1. Select the first page that requires an illustration, or the page number specified by the user.
2. Read the current narrative row and relevant explorer details.
3. Locate the exact repository file `Bo_image.jpg`.
4. Build the complete page-specific prompt from the template below.
5. Present the exact, complete prompt in a single code block for easy copying. Do not require the user to run a script or download/import an image.
6. If Bo appears, remind the user to attach `Bo_image.jpg` in ChatGPT as the visual reference.
7. Stop and let the user generate the image in ChatGPT. Do not claim to have generated or inspected an image that the user has not provided.
8. If the user later shares the generated image and asks for review, inspect it against the artistic quality gate. If it fails or the user requests changes, revise only the prompt for the current illustration.
9. Do not proceed to another page until the user explicitly approves the current illustration.

Never interpret silence or a request for changes as approval. Approval applies only to the current illustration.

## Master character reference

`Bo_image.jpg` is the visual source of truth. Do not rely on a text description alone when the image is available.

Preserve Bo's:
- round head and lighter muzzle patch;
- two large square front teeth;
- round ears and small tuft of fur;
- striped scarf;
- small backpack;
- broad, flat, paddle-shaped tail;
- face, body proportions and overall silhouette.

Only pose, expression, orientation and placement may change. Do not change his clothing, accessories, teeth, tail shape or defining proportions.

If the file is missing or inaccessible, stop and ask the user to upload it or connect the repository. Do not substitute another beaver or create an approximation.

## Illustration-only output contract — critical

The output must contain **only the artwork intended for the upper illustration frame**.

Do NOT create:
- a complete book page;
- a page border, frame or rectangular panel;
- a text frame or caption box;
- story text, titles, letters, numbers or labels;
- page numbers, watermark, signature or decorative typography;
- white margins designed for a finished page;
- any layout elements intended for the compiler.

The image should be a clean illustration on a plain white background, ready to be placed inside the upper frame by `bo-page-compiler`.

Do not reserve a lower text area inside the illustration canvas. The compiler creates that area separately.

## Image format

- Use the illustration aspect ratio and pixel dimensions requested by the compiler, if supplied.
- If no dimensions are supplied, create a portrait-friendly illustration asset at a high resolution suitable for placement in a portrait 8.5 × 11 inch page.
- Pure white background.
- Black-and-white line art only.
- No bleed, frame, border or page layout.
- Keep the main subject and landmark comfortably inside the image edges so the compiler can crop/fit it without cutting important details.

## Art direction

- Audience: children aged 3–6.
- Thick, smooth, consistent black outlines.
- Closed shapes wherever practical.
- Large, open areas easy to colour with crayons.
- Bo and friendly animals: simple, rounded, cartoon-like.
- Landmark or landscape: recognisable real-world silhouette and defining features, moderately realistic proportions with simplified details.
- The landmark may be more detailed than Bo but must remain easy to colour.
- Clear visual hierarchy and uncluttered composition.
- Use only the elements required by the narrative row.

No colour, grey tones, shading, gradients, hatching, realistic textures, fur/feather micro-detail, tiny ornaments, dense patterns or large solid black areas. Small black eyes and noses are acceptable.

## Prompt template

Present the completed prompt for the user to paste into ChatGPT verbatim, attaching `Bo_image.jpg` there as the reference when Bo appears. Do not send an unfinished template or silently alter the prompt. After presenting it, stop and wait for the user.

Create the **[PAGE / DESTINATION NAME]** illustration for a children's colouring book for ages 3 to 6.

IMPORTANT: Generate the illustration artwork ONLY. Do not create a book page, layout, frame, border, panel, text area, caption, title, typography, letters, numbers, page number, watermark or signature. The separate page compiler will add the frames and story text later.

CHARACTER REFERENCE: Use the attached master reference image `Bo_image.jpg` as the authoritative visual reference for Bo. Keep his round head, lighter muzzle patch, two large square front teeth, round ears, small tuft of fur, striped scarf, small backpack, body proportions and broad flat paddle-shaped tail consistent with the reference. Only his pose, expression, orientation and placement may change. Do not redesign him.

SCENE: [Translate the narrative row's graphic-content summary into a precise composition. Specify Bo's pose and placement, landmark silhouette, foreground/background, and the local animal or companion only when supported by the research.]

LOCATION ACCURACY: [Describe verified distinctive features of the actual monument, landscape or environment. Preserve its recognizable silhouette and defining details while simplifying it for young colourists.]

COMPOSITION: [Use the aspect ratio supplied by the compiler. Keep all important subjects fully visible, with comfortable space around the edges. No cropping of Bo, animals or the landmark.]

LINE ART: Thick, smooth, clean black outlines; closed shapes; large open colouring areas. Bo and animals remain simple, friendly and rounded. The landmark has moderately realistic proportions with simplified details. Pure white background.

DO NOT INCLUDE: any text, letters, numbers, frames, borders, panels, captions, titles, page layout, colour, grey tones, shading, gradients, hatching, realistic textures, intricate patterns, clutter, large solid black areas except eyes and noses, cropped characters, cropped landmarks or cropped objects.

After generating, check that Bo matches the attached reference, the location is recognisable and accurate, all required scene elements are present, the composition fits the requested aspect ratio, and the result contains artwork only. If anything fails, revise and regenerate this same illustration.

## Page-specific rules

- **Destination:** Bo and the landmark must both be prominent. Add at most one local animal/companion unless the narrative row explicitly requires more.
- **Friends page:** Follow the exact count, species and arrangement in the narrative row. No extra animals.
- **Map page:** Draw only the map artwork and symbols; no title lettering or labels unless the narrative specifically requires a non-text visual symbol. The compiler adds any wording.
- **Treasure page:** Follow the established story reveal. Do not invent a different treasure.
- **Favourite-place activity:** Create only the small illustration element, if any. Leave blank drawing-space decisions to the compiler.
- **Certificate:** Create only the illustration artwork or decorative non-text motifs. Never render certificate wording.

## Artistic quality gate

- [ ] Correct page and scene from the narrative row.
- [ ] Bo matches the actual `Bo_image.jpg` reference.
- [ ] Landmark/environment is recognisable and factually grounded.
- [ ] Correct animal/companion and exact count.
- [ ] Clean black outlines and large colourable spaces.
- [ ] Pure white background; no colour, grey or shading.
- [ ] No text, typography, frames, borders or page-layout elements.
- [ ] No important subject is cropped.
- [ ] Image aspect ratio matches the compiler's request.

If any check fails, revise the same illustration before presenting it.

## Review response

Show only the current illustration asset and ask:

"Illustration for page [N] is ready. Do you approve it, or would you like any changes?"

Do not create or preview the next illustration until explicit approval.

If approved, mark the illustration approved and pass its asset plus the matching narrative row to `bo-page-compiler`. Do not add the frames or text yourself.
