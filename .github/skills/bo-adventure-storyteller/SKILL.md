---
name: bo-adventure-storyteller
description: Creates a complete continent-based Bo the Beaver colouring storybook plan using 15 destinations selected by continental-explorer or destinations supplied by the user.
---

# Bo's Adventure Storyteller

## Mission

Create a complete, coherent, child-friendly colouring-book story starring **Bo the beaver**, travelling through a user-specified continent. Preserve the spirit and recognizable narrative architecture of *Bo's Big Adventure Across Europe* / *La grande aventure de Bo à travers l’Europe*, but create an original journey with new locations, clues, interactions and text.

You are a children's story architect and colouring-book art director. When the user has not supplied destinations, use all destinations selected by the companion skill `continental-explorer`; do not ask the user to approve or choose from its list.

## Required workflow — do not skip

### Stage 1 — collect the continent
Required input: `continent`.

Optional inputs:
- `language`: default English.
- `audience_age`: default 3–6.
- `destination_count`: default 15 when the user has not supplied a destination list; use the number the user supplied when they provide their own list.
- `story_length`: default comparable to the source book; may be adjusted.
- `tone`: default warm, playful, adventurous, reassuring.
- `format_constraints`: page size, trim, bleed, text placement, page count, print requirements.
- `continuity_notes`: prior Bo-book details or series canon.

If "America" or another label is geographically ambiguous, ask whether the user means North America, South America, or the Americas. Ask only for information essential to proceed.

### Stage 2 — select destinations without an approval pause
If the user has not supplied a destination list, call or delegate to `continental-explorer` with:
- the continent;
- requested destination count (default 15);
- language;
- any inclusion/exclusion constraints.

The explorer returns a short JSON list of selected destinations, not a research dossier. Treat every listed destination as selected and continue directly to the story; do not present the list as options, ask for approval, or wait for the user to choose.

If the user supplied their own destinations, use those as the authoritative list and do not invoke the explorer unless they request additional choices.

If the skill cannot be invoked in the current environment:
1. State clearly that the explorer skill was not available.
2. Ask only for essential missing destination details or offer to verify destinations, rather than inventing an explorer result.
3. Do not pretend a handoff occurred.

### Stage 3 — validate selected destinations
Treat the user's supplied destinations, or the explorer's full selected list, as the authoritative destination list. Check that destinations fit the requested continent and constraints. Briefly verify facts about selected places as needed for an accurate story; do not require a continent-wide dossier or repeat exhaustive research. If an explorer-selected destination is ambiguous or cannot be verified, replace it with a credible, visually distinct alternative that meets the same constraints; do not pause for approval. Ask only if a user-supplied destination is ambiguous and cannot be resolved.

### Stage 4 — design the story arc
Use the source book's narrative DNA, not its exact wording or scene sequence.

#### Core story DNA to preserve
1. **Familiar hero:** Bo is a friendly young beaver with a clear, consistent silhouette.
2. **Personal motivation and series continuity:** The previous European adventure began when Bo discovered his Grandpa's map and travelled to Europe. For a new continent, do not retell that discovery or repeat the Europe trip: open with the same map calling, glowing, or otherwise inviting Bo on a new adventure. The map must clearly summon him to the continent the user selected.
3. **Simple mission:** follow the map across the continent to find a treasure.
4. **Repeatable page engine:** at each destination, Bo briefly observes the current place and meets a different animal associated with that country. They talk, and the animal gives a simple riddle pointing to the next selected destination without naming it.
5. **Learning through play:** children notice shapes, count features, imitate sounds/movements, match symbols or answer simple questions.
6. **Escalation:** the clues gradually form a pattern or reveal what the treasure really means.
7. **Payoff:** Bo finds a chest or final discovery. The treasure should resolve the emotional promise of the story; it need not be gold.
8. **Warm ending:** celebrate friendship, curiosity and what Bo learned; include a recap/activity and a completion certificate.

#### Two-page opening and complete story arc
- Include exactly **two consecutive opening story pages** before the first destination page; a cover is separate and does not count toward these two pages.
- Opening page 1 establishes that Grandpa's familiar map is calling Bo to a new adventure. Opening page 2 shows Bo accepting the invitation and setting off toward the selected continent, with a child-friendly hint of the treasure or question driving the journey. Write complete child-facing text for both pages.
- Make the story feel complete: the map's call is the beginning, the selected destinations and clues build toward a clear climax, and the final narrative page shows Bo discovering the treasure. Resolve the map's promise and finish that page with one brief, child-friendly moral about the journey (such as curiosity, friendship, or sharing); make it part of the ending rather than a preachy lecture. Recaps, activities, or certificates may follow as non-narrative extras, but do not continue the plot after the treasure ending.

The new story must feel like a fresh adventure. Do not reuse the European book's exact jokes, sentences, clue sequence, animal encounters or destination order.

#### Bo character continuity
Unless the user supplies updated character canon, preserve:
- cartoon beaver with a round head;
- lighter muzzle patch;
- two large square front teeth;
- round ears and a small tuft of fur;
- striped scarf (three stripes);
- small backpack;
- broad, flat, paddle-shaped tail.

Bo should look like the same character on every page. His outfit and proportions must not drift. He is curious, kind, brave in an age-appropriate way, and sometimes surprised or silly. Avoid making him sarcastic, frightening or overly clever for the target age.

### Stage 5 — create a meaningful route
- Use every selected destination unless the user asks for a shorter book.
- Put locations in an understandable travel sequence, minimizing implausible jumps where possible.
- If the continent is very large, use a magical map, train, boat, plane or other child-friendly transitions to make the journey credible.
- Do not imply that Bo physically walks between distant places without a transition.
- Every stop must contribute something different: a new visual scene, clue, friend, action or learning moment.
- Give Bo one country-typical animal companion at every destination. Assign a **different species to every stop across the entire route**: never reuse an animal, including between different countries or between multiple stops in one country. Choose an animal credibly and recognizably associated with that stop's country; verify the association and habitat, and record the unique assignment in the destination mapping. Place it in a setting or context where it belongs; never imply that an animal is native to, or naturally lives at, a monument or habitat where it does not. If no suitable, accurate, unused animal can be established, ask the user how to proceed rather than inventing or repeating one.
- Avoid stereotypes and cultural tokenism. The setting, not a caricature, should communicate the place.

### Stage 6 — write page content
Default audience: ages 3–6. Every child-facing text in the book—not only destination pages—must use language suitable for children ages 3–6. Use very short sentences, familiar concrete words, simple grammar, gentle repetition and one clear idea at a time. Make the text easy to understand when read aloud. Avoid abstract explanations, long or complicated sentences, difficult idioms, and riddles that require knowledge the child has not been given.

Each destination page must use this child-facing text sequence:
1. **Place:** In one short, natural sentence, identify the exact place and country while showing Bo's reaction. Vary the sentence structure from page to page; do not repeatedly start with "Bo is at..." or "Bo está en...". For example: "Bo gasps at snowy Mount Fuji in Japan!" Keep the place and country clear, but let the sentence feel lively and natural.
2. **Stamp:** Include the standalone sound word **"Stamp!"** followed by one short sentence saying that a simple symbol appears on Bo's map. Choose one clear, drawable symbol tied to both the country and the specific place (for example, a bell, tower, or mountain). Keep it to a single simple element, not a detailed scene or a collection of symbols. Assign a different symbol at each stop; verify its connection and avoid unsupported cultural associations or stereotypes. Include this map-stamp beat on every destination page.
3. **Animal and clue:** The unique local animal speaks directly to Bo and gives a short, child-friendly clue to the next selected place. The clue should point to one recognizable feature without naming the place, and be solvable from the story or picture; avoid difficult riddles or abstract wordplay. Do not insert unrelated narration between the stamp and this animal line. At the final destination there is no next place: the animal instead helps Bo discover or reach the treasure, without inventing another destination.
4. **Interaction:** End with one simple question or action for the child, tied to something visible on the page (for example, "Can you point to Mount Fuji's snowy peak?"). Make it easy to answer by looking, pointing, counting a small number, or imitating a sound or movement; do not rely on reading ability.

Keep the sequence—varied place sentence, "Stamp!" and map symbol, animal's clue or final treasure cue, child interaction—consistent on every destination page. The location sentence must name both the exact place and its country. Keep each beat very brief and use age-appropriate words. Vary the place sentence, the symbol, animal dialogue and interaction so the pages do not sound mechanically repeated.

Vary sentence openings, animal interactions, sound effects and prompts. Repetition should create familiarity, not monotony.

Keep factual text minimal and correct. Do not overload young readers with dates, political history, long names or complex explanations. Pronounceable place names are welcome, but do not distort them into inaccurate names.

### Stage 7 — ending and educational activities
Include, as appropriate:
- treasure discovery page;
- recap of symbols or stamps collected;
- group/farewell page featuring the friends Bo met;
- favourite-place drawing page;
- official young-explorer certificate.

The final treasure should connect to the theme of discovery, friendship, curiosity or shared memories. Do not make the story's moral preachy.

## Output format — mandatory

The main deliverable is a **page-by-page table with one row per content page**. Do not provide only a synopsis.

## Required planning document

- Save the complete page plan to `dossier description/<continent-slug>/plan-de-paginas.md`, relative to the repository root. Create the directory if it does not exist. Use the same continent slug convention as the repository's asset paths (lowercase, normalized accents, hyphens between words); for example, `dossier description/asia/plan-de-paginas.md`.
- The Markdown document is a required deliverable, not an optional export. Include the complete page-by-page table with all required columns and page text, followed by the story concept, destination mapping, continuity and illustration bible, child-interaction audit, fact-check and sensitivity notes, and production notes.
- Add a short header identifying the continent, language, audience age, destination count, and any relevant user constraints. Keep all sections in the language requested for the story.
- Also present the complete table and supporting deliverables in the response, and provide a link to the saved document. Do not claim it was saved unless the file was actually written successfully.
- When the user gives new instructions, corrections, or approved content that changes the plan, read the existing document first and update this same file in place. Regenerate the affected table rows and all dependent sections so they remain consistent; preserve unchanged approved details and unrelated user notes. Do not create a second competing plan or append duplicate outdated tables. Then return the updated document link and summarize what changed.
- If instructions change a destination, animal, route, text, page order, or production constraint, propagate the change everywhere it appears in the document (including the mapping, illustration notes, interactions, and production notes).

Use these columns exactly:

| Page | Page role | Graphic content summary | City / region | Country | Monument / landscape / setting | Local animal | Text appearing on the page | Impact on the story |
|---|---|---|---|---|---|---|---|---|

Requirements:
- **Page:** sequential content-page number. If print pagination includes blank reverse sides, explain that separately; do not silently count blanks as story pages.
- **Page role:** cover, opening, map, destination, treasure, recap, activity, certificate, etc.
- **Graphic content summary:** concise but drawable composition. For each destination, show Bo briefly observing the current place, the unique animal speaking to him, and the map with the simple stamp symbol appearing. Keep the map and stamp small enough not to compete with the landmark; Bo does not have to hold the map. If the riddle has a clear visual cue, describe it without adding text or prematurely depicting the next destination itself. Include foreground/background and the main action where useful. Show the map on other pages only when that row's scene requires it.
- **City / region:** actual city or region; use "en route" or "not applicable" for non-location pages.
- **Country:** actual country; use "multiple" or "not applicable" where appropriate.
- **Monument / landscape / setting:** exact researched place; do not replace it with a generic label.
- **Local animal:** name the distinct animal for this destination and briefly identify its credible association with the country and why the depicted setting is appropriate. Do not reuse an animal at another stop or misrepresent its range/habitat. Use "not applicable" on non-destination pages.
- **Text appearing on the page:** provide the complete child-facing text, not a placeholder. For every destination, follow the exact order: varied sentence naming the place and country; "Stamp!" plus a simple map-symbol appearance; the animal's brief clue to the next selected destination (or a treasure cue at the final stop); and one simple child interaction. Keep all wording suitable for ages 3–6 and short enough to fit the intended text panel.
- **Impact on the story:** explain what the page changes: introduces mission, reveals clue, builds friendship, advances the route, raises anticipation, resolves the mystery, or celebrates learning.

For destination pages, preserve the required mini-structure: Bo reacts to the current place in a varied sentence naming the place and country; "Stamp!" introduces one simple, distinct map symbol tied to that country and place; the unique local animal gives the next-place riddle; and the text ends with a simple child interaction. The riddle must match a recognisable feature of that destination without naming it. The final stop has no next-destination riddle and instead leads into the established treasure ending. Every destination illustration must show the map during the stamp moment and the selected simple symbol; other pages show the map only when their row calls for it.

The two opening pages must appear as the first two narrative rows in the table (after a cover row, if one is included). Every child-facing text must be suitable for ages 3–6. On every destination row, the complete child-facing text must use the required four-beat sequence and naturally name both the exact place and its country before the stamp and animal clue. The final narrative page must show the treasure discovery, resolve the adventure, and include the brief moral; any following activities are non-narrative extras.

## Additional deliverables after the table

### 1. Story concept
- Working title.
- One-sentence premise.
- Short synopsis (150–250 words).
- Central emotional message.
- Explanation of how the treasure reveal pays off the journey.

### 2. Destination-to-story mapping
A compact list mapping each explorer destination ID to its page number, distinct animal, narrative purpose and riddle/stamp. Every selected destination must be accounted for, or an explicit reason must be given for omitting one. State which recognisable feature the riddle points to; the riddle itself must not name the next destination.

### 3. Continuity and illustration bible
Specify:
- Bo's fixed character design;
- recurring props (backpack, scarf, stamps, chest; show the map only on pages that need it);
- line-art style: black outlines, white background, no grayscale or colour fills unless requested;
- simple, open shapes and generous colouring areas;
- visual hierarchy: Bo and the landmark must both be easy to identify;
- page composition and recurring layout;
- how to keep Bo's scale, face, scarf, tail and backpack consistent;
- cultural and architectural accuracy notes for illustrators.

### 4. Child interaction audit
List the interaction on each destination page and check that:
- prompts are understandable to ages 3–6;
- tasks are achievable from the illustration;
- prompts vary (count, find, point, imitate, compare, draw);
- no page relies on reading ability alone.

### 5. Fact-check and sensitivity notes
List any location details, animal associations, cultural representations or spellings that the illustrator/writer must verify. Briefly check reliable sources for the selected monuments when needed; distinguish verified facts from creative choices.

### 6. Production notes
Recommend a practical page count and note:
- story-page count versus blank reverse pages;
- portrait trim and safe margins if supplied;
- text-panel space;
- whether a page needs a full-bleed illustration (default: no, unless requested);
- pages that should be kept especially uncluttered for young colourists.

## Narrative quality gate

Before finalizing, verify all of the following:

- [ ] The user selected every destination or supplied it directly.
- [ ] The user's geographic constraints are respected.
- [ ] The first two story pages form the complete opening: Grandpa's map calls Bo to a new continent adventure, and Bo accepts and sets off.
- [ ] The story has a clear beginning, middle, climax and ending.
- [ ] The map/clue mechanism is consistent and pays off.
- [ ] Each destination has a distinct visual composition and story function.
- [ ] All child-facing text is suitable for ages 3–6: short, concrete, easy to read aloud and understand.
- [ ] Every destination follows the exact varied place-and-country sentence, "Stamp!" and simple map symbol, animal clue/treasure cue, and child-interaction sequence.
- [ ] Place sentences vary naturally instead of repeating "Bo is at..." or an equivalent formula on every page.
- [ ] Every destination's map symbol is simple, tied to both its country and place, and not reused elsewhere on the route.
- [ ] Every destination names its exact place and country in its child-facing text before the stamp and animal's clue.
- [ ] Every destination has a unique, country-typical animal species not used anywhere else in the route, in a plausible setting, and the animal converses with Bo.
- [ ] Every non-final destination has a simple, indirect riddle about the next selected destination and its recognisable feature; the final stop leads to the ending instead.
- [ ] Each destination's illustration shows Bo observing the current place, visibly interacting with its animal, and the map's stamp moment; other pages show the map only when their scene requires it.
- [ ] Every destination page includes complete child-facing text and a child interaction.
- [ ] Each destination's interaction is simple and answerable by looking, pointing, counting a small number, or imitating.
- [ ] Bo's appearance and personality remain consistent.
- [ ] Local animals are not falsely presented as native or typical.
- [ ] Language is age-appropriate, natural and read-aloud friendly.
- [ ] The treasure reveal is emotionally satisfying, resolves the map's call, and ends with a brief, child-friendly moral.
- [ ] The requested page-by-page table is complete.
- [ ] The story is original and does not copy the source book's wording.

If any check fails, revise before delivering.
