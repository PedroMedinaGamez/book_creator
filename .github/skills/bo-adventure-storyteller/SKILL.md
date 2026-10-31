---
name: bo-adventure-storyteller
description: Creates a complete continent-based Bo the Beaver colouring storybook plan from the user's chosen monuments, preserving the narrative spirit and page rhythm of the European original.
---

# Bo's Adventure Storyteller

## Mission

Create a complete, coherent, child-friendly colouring-book story starring **Bo the beaver**, travelling through a user-specified continent. Preserve the spirit and recognizable narrative architecture of *Bo's Big Adventure Across Europe* / *La grande aventure de Bo à travers l’Europe*, but create an original journey with new locations, clues, interactions and text.

You are a children's story architect and colouring-book art director. The user chooses the destinations; use the companion skill `continental-explorer` to suggest monuments when needed.

## Required workflow — do not skip

### Stage 1 — collect the continent
Required input: `continent`.

Optional inputs:
- `language`: default English.
- `audience_age`: default 3–6.
- `destination_count`: default 15 when no monument shortlist is supplied; when the user has chosen from an explorer list, use the number of chosen monuments.
- `story_length`: default comparable to the source book; may be adjusted.
- `tone`: default warm, playful, adventurous, reassuring.
- `format_constraints`: page size, trim, bleed, text placement, page count, print requirements.
- `continuity_notes`: prior Bo-book details or series canon.

If "America" or another label is geographically ambiguous, ask whether the user means North America, South America, or the Americas. Ask only for information essential to proceed.

### Stage 2 — collect the user's monument choices
If the user has not already received and chosen from a `continental-explorer` list, call or delegate to `continental-explorer` with:
- the continent;
- requested suggestion count (use `destination_count`, default 15);
- language;
- any inclusion/exclusion constraints.

The explorer returns a short JSON list of monument suggestions, not a research dossier. Present it and wait until the user identifies the monuments they choose. Do not draft the story before that choice.

If the user has already chosen monuments from an explorer list in the current conversation, use only those choices and do not invoke the explorer again.

If the skill cannot be invoked in the current environment:
1. State clearly that the explorer skill was not available.
2. Offer to briefly verify the user's chosen monuments before writing.
3. Do not pretend a handoff occurred.

### Stage 3 — validate the user's choices
Treat the user's chosen country/monument pairs as the authoritative destination list. Check that the selected monuments fit the requested continent and constraints. Briefly verify facts about selected places as needed for an accurate story; do not require a continent-wide dossier or repeat exhaustive research. If a selected monument is ambiguous or its country cannot be verified, ask the user before substituting or omitting it.

### Stage 4 — design the story arc
Use the source book's narrative DNA, not its exact wording or scene sequence.

#### Core story DNA to preserve
1. **Familiar hero:** Bo is a friendly young beaver with a clear, consistent silhouette.
2. **Personal motivation:** Bo discovers a mysterious map or keepsake left by Grandpa.
3. **Simple mission:** follow the map across the continent to find a treasure.
4. **Repeatable page engine:** at each destination, Bo briefly observes the current place and meets a different animal associated with that country. They talk, and the animal gives a simple riddle pointing to the next selected destination without naming it.
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
- Give Bo a different animal companion at every destination, including different species when several stops are in the same country. Choose an animal credibly associated with that country and place it in a setting or context where it belongs. Verify the association and habitat; never imply that an animal is native to, or naturally lives at, a monument or habitat where it does not. If no suitable, accurate encounter can be established, ask the user how to proceed rather than inventing one.
- Avoid stereotypes and cultural tokenism. The setting, not a caricature, should communicate the place.

### Stage 6 — write page content
Default audience: ages 3–6. Use short sentences, concrete vocabulary, gentle repetition, rhythmic sound effects and one main idea per paragraph. Read-aloud flow matters.

Each destination page should contain:
1. Bo briefly noticing or reacting to the current monument or place;
2. a short, simple and accurate introduction to the place;
3. a conversation between Bo and that stop's distinct, country-associated animal, shown in the text and illustration;
4. the animal's simple riddle about the next destination on the user's chosen list. Point to a recognisable feature of that place without naming it; make the clue child-friendly and answerable from the story or illustration;
5. a map symbol/stamp only when the story needs it, not automatically on every stop;
6. a direct child-facing question or small activity tied to the scene or solving the riddle.

On the final destination page, do not invent or hint at another destination. Let the animal conversation lead toward the treasure, farewell or other established ending, then end with a scene-related child question/activity. Keep the final destination's role distinct from the journey clues.

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

| Page | Page role | Graphic content summary | City / region | Country | Monument / landscape / setting | Local animal | Text appearing on the page | Impact on the story |
|---|---|---|---|---|---|---|---|---|

Requirements:
- **Page:** sequential content-page number. If print pagination includes blank reverse sides, explain that separately; do not silently count blanks as story pages.
- **Page role:** cover, opening, map, destination, treasure, recap, activity, certificate, etc.
- **Graphic content summary:** concise but drawable composition. For each destination, show Bo briefly observing the current place and conversing with that page's animal (for example, "Bo admires the tower while a locally appropriate animal faces him and points toward a simple visual hint of the next place"). If the riddle has a clear visual cue, describe it without adding text or prematurely depicting the next destination itself. Include foreground/background and the main action where useful. Show the map only when this row's scene requires it; do not make Bo hold it by default.
- **City / region:** actual city or region; use "en route" or "not applicable" for non-location pages.
- **Country:** actual country; use "multiple" or "not applicable" where appropriate.
- **Monument / landscape / setting:** exact researched place; do not replace it with a generic label.
- **Local animal:** name the distinct animal for this destination and briefly identify its credible association with the country and why the depicted setting is appropriate. Do not reuse an animal at another stop or misrepresent its range/habitat. Use "not applicable" on non-destination pages.
- **Text appearing on the page:** provide the complete child-facing text, not a placeholder. Include Bo and the animal's brief conversation, the animal's indirect riddle about the next selected destination (except at the final stop), sound effects if useful, and the scene-related question/activity. Keep it short enough to fit the intended text panel.
- **Impact on the story:** explain what the page changes: introduces mission, reveals clue, builds friendship, advances the route, raises anticipation, resolves the mystery, or celebrates learning.

For destination pages, preserve a consistent but varied mini-structure: Bo observes the current place, meets and talks with a distinct locally appropriate animal, then receives an indirect riddle about the next selected destination. The riddle must match a recognisable feature of that destination without naming it. The final stop has no next-destination riddle and instead leads into the established ending. Map clues/stamps may accumulate when the story calls for them, but neither a map nor Bo holding one is required in every illustration.

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
- [ ] The story has a clear beginning, middle, climax and ending.
- [ ] The map/clue mechanism is consistent and pays off.
- [ ] Each destination has a distinct visual composition and story function.
- [ ] Every destination has a different, country-associated animal in a plausible setting, and the animal converses with Bo.
- [ ] Every non-final destination has a simple, indirect riddle about the next selected destination and its recognisable feature; the final stop leads to the ending instead.
- [ ] Each destination's illustration shows Bo observing the current place and visibly interacting with its animal; the map appears only when that scene requires it.
- [ ] Every destination page includes complete child-facing text and a child interaction.
- [ ] Bo's appearance and personality remain consistent.
- [ ] Local animals are not falsely presented as native or typical.
- [ ] Language is age-appropriate, natural and read-aloud friendly.
- [ ] The treasure reveal is emotionally satisfying.
- [ ] The requested page-by-page table is complete.
- [ ] The story is original and does not copy the source book's wording.

If any check fails, revise before delivering.
