---
name: bo-page-artist
description: Designs a detailed, production-ready prompt for one accurate black-and-white Bo storybook illustration, including scene composition, location details, character reference and strict art constraints. Hands it to creadora-imagen-ia for API generation.
---

# Bo Page Artist

## Mission

Create the **illustration artwork only** for the current page in a Bo the Beaver children's colouring book.

This skill is the artistic production stage. It must not design or assemble the finished page. A separate skill, `bo-page-compiler`, is responsible for adding the frames, exact story text, margins and print layout.

Design a complete, page-specific prompt that directs an image-generation model to create the approved illustration accurately and consistently. Hand the exact prompt and required metadata to `creadora-imagen-ia`, which sends the prompt and reference image to the OpenAI Images API, downloads the result and stores a versioned PNG. This skill designs the image and prompt; it does not call the API or claim to generate the image itself. The repository file `Bo_image.jpg` is the authoritative visual reference and is sent with every request; the prompt must explicitly say not to add Bo to a scene unless the approved narrative row includes him.

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

## One-illustration prompt and approval workflow

1. Select the first page that requires an illustration, or the page number specified by the user.
2. Read the current narrative row and relevant explorer details.
3. Locate the exact repository file `Bo_image.jpg`.
4. Design and check the complete page-specific prompt using the art direction, prompt template and quality gate below. Resolve every placeholder and specify the exact composition; do not make the API skill invent missing scene details.
5. Hand the exact final prompt, continent, country, monument, repository `Bo_image.jpg`, and (for a correction) the previous generated image to `creadora-imagen-ia`. Do not alter the prompt during handoff.
6. The API skill must request user confirmation before any paid API call unless the user has already explicitly authorized generation in the current request. Do not claim generation has started until the request is confirmed and executed.
7. Review the returned image against the narrative row and artistic quality gate. Do not claim that a prompt or API response guarantees a perfect result.
8. If the user requests a correction, identify the specific defects, revise the prompt to fix only those defects, and explicitly identify `Bo_image.jpg` as the character reference and the prior generated image as the base composition. Preserve every approved element not named for correction. Pass the revised prompt, previous image and `Bo_image.jpg` to `creadora-imagen-ia`. Corrections create a new version; never overwrite the prior image.
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

- Every illustration must use the same moderately portrait **2:3 width-to-height ratio and 1024 × 1536 px canvas**. Do not vary the dimensions between pages or revisions.
- The compiler places this image proportionally, centered inside the approximately 1779 × 2349 px upper frame on a 2550 × 3300 px page. Preserve the full illustration: do not crop or distort it. The frame may have even white side insets because its ratio differs slightly from the illustration ratio.
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
- For destination pages, when specified by the approved story row, make the conversation visible through the characters' expressions, facing direction and gestures: Bo observes the current place and listens or responds to its distinct, locally appropriate animal. If the row describes a drawable hint for the animal's riddle, show that hint as a simple, non-text visual cue without depicting the next destination itself. Do not add speech balloons or text.
- Landmark or landscape: faithfully represent the real place's recognizable silhouette, defining architectural or natural features, relative scale, and plausible proportions. Make the place more realistic and accurate in its physical form, while simplifying small details for colouring; do not invent, merge, or distort distinctive features.
- The landmark may be more detailed than Bo but must remain easy to colour.
- Clear visual hierarchy and uncluttered composition.
- Use only the elements required by the narrative row.
- Do not add the map as a recurring prop. Include it only when the current narrative row explicitly requires it; Bo does not need to hold it whenever it appears. Any map shown as a prop must obey the same approved scope and exclusion constraints as a map page.
- Compose the scene deliberately: establish one focal action, a readable foreground/middle-ground/background, clear relative scale, and a camera angle that shows both Bo's interaction and the landmark's identifying silhouette. Keep all important forms separated and fully inside the image.
- Make the current place immediately recognizable through a few verified architectural or landscape features, not invented ornament or excessive background detail. Its structure and proportions should be reasonably true to the real monument or landscape, even though the rendering is clean, simplified line art rather than photorealistic. Use accurate local context for animals; do not imply an animal belongs at a monument or habitat where it would not naturally occur.
- For a conversation, use eye-lines, body orientation and gestures to make it legible without speech bubbles, lettering or symbols that could be mistaken for text. For a riddle clue, use only a simple visual hint described in the approved row, without accidentally showing or naming the next destination.
- Adapt the layout to the requested image ratio and keep a comfortable white safety area around the subjects. Do not let the reference-image composition dictate the new scene's crop or background.

No colour, grey tones, shading, gradients, hatching, realistic textures, fur/feather micro-detail, tiny ornaments, dense patterns or large solid black areas. Small black eyes and noses are acceptable.

## Prompt template

Produce the completed prompt for the image-generation API skill. Do not leave placeholders or ask that skill to invent visual details. `creadora-imagen-ia` sends `Bo_image.jpg` separately as a reference image; when Bo appears, explicitly tell the model to use it as the character-design reference, not as the scene to copy. If the story row does not include Bo, explicitly instruct the model not to add him despite the reference input.

Create the **[PAGE / DESTINATION NAME]** illustration for a children's colouring book for ages 3 to 6.

IMPORTANT: Generate the illustration artwork ONLY. Do not create a book page, layout, frame, border, panel, text area, caption, title, typography, letters, numbers, page number, watermark or signature. The separate page compiler will add the frames and story text later.

CHARACTER REFERENCE: The API request includes the repository image `Bo_image.jpg` as a reference input. Use it as the authoritative visual reference for Bo's identity only. Keep his round head, lighter muzzle patch, two large square front teeth, round ears, small tuft of fur, striped scarf, small backpack, body proportions and broad flat paddle-shaped tail consistent with it. Only his pose, expression, orientation and placement may change. Do not copy the reference image's pose or background, and do not redesign Bo.

SCENE AND ACTION: [Describe the exact approved story scene, its single focal action, Bo's pose and expression, the other character's action, and how the interaction reads visually. Include only narrative-approved elements.]

COMPOSITION: Use the fixed 1024 × 1536 px, 2:3 portrait illustration canvas used on every page. The compiler will center it, without cropping or distortion, inside the approximately 1779 × 2349 px upper frame of the 2550 × 3300 px KDP page; a small, even white inset at the sides is acceptable. Specify camera/viewpoint, subject placement and scale, recognizable landmark silhouette, and uncluttered foreground/middle-ground/background. Keep all important details fully visible with safe space around the edges.

LOCATION AND ANIMAL ACCURACY: [Name verified distinctive features of the actual monument or environment and the specified animal. Represent the real place with recognizable, reasonably accurate structure and proportions, simplified for colouring; do not invent or distort landmark features. Place the animal only in a plausible country/habitat context. Do not imply unsupported wildlife associations.]

LINE ART AND COLOURING: Pure white background; black-and-white line art only. Thick, smooth, consistent black outlines; closed shapes wherever practical; large open areas easy to colour. Keep Bo and friendly animals simple, rounded and consistent with the reference. Use recognizable but simplified landmark details and a clear visual hierarchy.

DO NOT INCLUDE: any text, letters, numbers, speech bubbles, frames, borders, panels, captions, titles, page layout, colour, grey tones, shading, gradients, hatching, realistic textures, intricate patterns, clutter, large solid black areas except small facial details, extra animals or props, unsupported wildlife, cropped characters, cropped landmarks or cropped objects. Include a map only if this exact story row requires it; if shown, obey all approved geographic exclusions.

Before generation, ensure the prompt matches the approved narrative row and verified research. After generation, the artist must check that Bo matches the reference, the location is recognizable, animals and props are correct, the composition is drawable and uncluttered, and the result contains artwork only. If anything fails, revise this same prompt for a new version.

## Page-specific rules

- **Destination:** Bo, the current landmark and the distinct animal specified by the story row must all be clear. Show Bo briefly observing the landmark and visibly conversing with the animal through pose and expression. Use at most one local animal/companion unless the narrative row explicitly requires more. Respect the animal's verified country association and habitat; do not place it in an implausible setting. Do not add the map unless the row calls for it.
- **Friends page:** Follow the exact count, species and arrangement in the narrative row. No extra animals.
- **Map page:** Draw only the map artwork and symbols; no title lettering or labels unless the narrative specifically requires a non-text visual symbol. The compiler adds any wording. Show only the continent or region specified in the approved story and its allowed scope—not a world map, other continents, or surrounding out-of-scope areas. Respect all inclusion and exclusion constraints exactly: do not depict excluded areas or show excluded countries/regions as destinations, labels, highlights, route stops, symbols or landmarks. Include only approved destinations. Do not infer an unclear map scope; ask the user to clarify before preparing the prompt.
- **Treasure page:** Follow the established story reveal. Do not invent a different treasure.
- **Favourite-place activity:** Create only the small illustration element, if any. Leave blank drawing-space decisions to the compiler.
- **Certificate:** Create only the illustration artwork or decorative non-text motifs. Never render certificate wording.

## Artistic quality gate

- [ ] Correct page and scene from the narrative row.
- [ ] Bo matches the actual `Bo_image.jpg` reference.
- [ ] Landmark/environment is recognisable and factually grounded.
- [ ] Correct animal/companion and exact count.
- [ ] Destination scene shows Bo observing the current place and interacting with the specified animal; the map appears only if the story row requires it.
- [ ] Any map is limited to the approved continent/region and obeys all inclusion and exclusion constraints.
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
