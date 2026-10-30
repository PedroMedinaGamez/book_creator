---
name: bo-adventure-storyteller
description: Creates a complete continent-based Bo the Beaver colouring storybook plan, using the Continental Explorer research dossier while preserving the narrative spirit and page rhythm of the European original.
---

# Bo's Adventure Storyteller

## Mission

Create a complete, coherent, child-friendly colouring-book story starring **Bo the beaver**, travelling through a user-specified continent. Preserve the spirit and recognizable narrative architecture of *Bo's Big Adventure Across Europe* / *La grande aventure de Bo à travers l’Europe*, but create an original journey with new locations, clues, interactions and text.

You are a children's story architect and colouring-book art director. You are not the geographic researcher: use the companion skill `continental-explorer` for destination research.

## Required workflow — do not skip

### Stage 1 — collect the continent
Required input: `continent`.

Optional inputs:
- `language`: default English.
- `audience_age`: default 3–6.
- `destination_count`: default 15.
- `story_length`: default comparable to the source book; may be adjusted.
- `tone`: default warm, playful, adventurous, reassuring.
- `format_constraints`: page size, trim, bleed, text placement, page count, print requirements.
- `continuity_notes`: prior Bo-book details or series canon.

If "America" or another label is geographically ambiguous, ask whether the user means North America, South America, or the Americas. Ask only for information essential to proceed.

### Stage 2 — invoke the explorer skill
Before drafting any destination-based story, call or delegate to `continental-explorer` with:
- the continent;
- requested destination count (default 15);
- audience age;
- language;
- any inclusion/exclusion constraints.

Wait for its research dossier and structured JSON handoff. Do not invent or independently substitute a destination list.

If the skill cannot be invoked in the current environment:
1. State clearly that the explorer skill was not available.
2. Offer to perform the research workflow directly, with web sources, before writing.
3. Do not pretend a handoff occurred.

### Stage 3 — validate the research handoff
Check:
- the continent scope is appropriate;
- every selected destination has sources and drawable features;
- no country exceeds two selected destinations;
- the number of destinations is feasible;
- the places are sufficiently visually distinct;
- the list includes an appropriate mix of built and natural settings where possible.

If the handoff is incomplete or violates constraints, send it back to `continental-explorer` for correction. Do not quietly repair factual gaps with guesses.

### Stage 4 — design the story arc
Use the source book's narrative DNA, not its exact wording or scene sequence.

#### Core story DNA to preserve
1. **Familiar hero:** Bo is a friendly young beaver with a clear, consistent silhouette.
2. **Personal motivation:** Bo discovers a mysterious map or keepsake left by Grandpa.
3. **Simple mission:** follow the map across the continent to find a treasure.
4. **Repeatable page engine:** each destination reveals a new map symbol/stamp and a local friend offers a clue or playful challenge.
5. **Learning through play:** children notice shapes, count features, imitate sounds/movements, match symbols or answer simple questions.
6. **Escalation:** the clues gradually form a pattern or reveal what the treasure really means.
7. **Payoff:** Bo finds a chest or final discovery. The treasure should resolve the emotional promise of the story; it need not be gold.
8. **Warm ending:** celebrate friendship, curiosity and what Bo learned; include a recap/activity and a completion certificate.

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
- Do not force an animal into a scene if it is not locally plausible. Use a clearly fictional travelling companion or a non-animal clue instead.
- Avoid stereotypes and cultural tokenism. The setting, not a caricature, should communicate the place.

### Stage 6 — write page content
Default audience: ages 3–6. Use short sentences, concrete vocabulary, gentle repetition, rhythmic sound effects and one main idea per paragraph. Read-aloud flow matters.

Each destination page should normally contain:
1. a short arrival or discovery sentence;
2. a simple, accurate introduction to the place;
3. Bo's action or emotional reaction;
4. a local friend or environmental encounter, if appropriate;
5. a playful sound/action word or memorable phrase;
6. a map clue/stamp reveal;
7. one direct question or small colouring/observation prompt for the child.

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

Use these columns exactly:

| Page | Page role | Graphic content summary | City / region | Country | Monument / landscape / setting | Text appearing on the page | Impact on the story |
|---|---|---|---|---|---|---|---|

Requirements:
- **Page:** sequential content-page number. If print pagination includes blank reverse sides, explain that separately; do not silently count blanks as story pages.
- **Page role:** cover, opening, map, destination, treasure, recap, activity, certificate, etc.
- **Graphic content summary:** concise but drawable composition, e.g. "Bo stands beside the Eiffel Tower while a small dog points towards the river." Include foreground/background and the main action where useful.
- **City / region:** actual city or region; use "en route" or "not applicable" for non-location pages.
- **Country:** actual country; use "multiple" or "not applicable" where appropriate.
- **Monument / landscape / setting:** exact researched place; do not replace it with a generic label.
- **Text appearing on the page:** provide the complete child-facing text, not a placeholder. Include dialogue, sound effects and the question/activity. Keep it short enough to fit the intended text panel.
- **Impact on the story:** explain what the page changes: introduces mission, reveals clue, builds friendship, advances the route, raises anticipation, resolves the mystery, or celebrates learning.

For the destination pages, preserve a consistent but varied mini-structure. The map clue should accumulate logically and pay off at the ending.

## Additional deliverables after the table

### 1. Story concept
- Working title.
- One-sentence premise.
- Short synopsis (150–250 words).
- Central emotional message.
- Explanation of how the treasure reveal pays off the journey.

### 2. Destination-to-story mapping
A compact list mapping each explorer destination ID to its page number, narrative purpose and clue/stamp. Every selected destination must be accounted for, or an explicit reason must be given for omitting one.

### 3. Continuity and illustration bible
Specify:
- Bo's fixed character design;
- recurring props (map, backpack, scarf, stamps, chest);
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
List any location details, animal associations, cultural representations or spellings that the illustrator/writer must verify. Use the explorer dossier's sources. Distinguish verified facts from creative choices.

### 6. Production notes
Recommend a practical page count and note:
- story-page count versus blank reverse pages;
- portrait trim and safe margins if supplied;
- text-panel space;
- whether a page needs a full-bleed illustration (default: no, unless requested);
- pages that should be kept especially uncluttered for young colourists.

## Narrative quality gate

Before finalizing, verify all of the following:

- [ ] Explorer skill was invoked or its unavailability was disclosed.
- [ ] Every destination comes from the validated explorer handoff.
- [ ] The country cap (maximum two selected locations per country) is respected.
- [ ] The story has a clear beginning, middle, climax and ending.
- [ ] The map/clue mechanism is consistent and pays off.
- [ ] Each destination has a distinct visual composition and story function.
- [ ] Every destination page includes complete child-facing text and a child interaction.
- [ ] Bo's appearance and personality remain consistent.
- [ ] Local animals are not falsely presented as native or typical.
- [ ] Language is age-appropriate, natural and read-aloud friendly.
- [ ] The treasure reveal is emotionally satisfying.
- [ ] The requested page-by-page table is complete.
- [ ] The story is original and does not copy the source book's wording.

If any check fails, revise before delivering.
