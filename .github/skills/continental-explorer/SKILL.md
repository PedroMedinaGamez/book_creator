---
name: continental-explorer
description: Researches a continent's most iconic, child-recognizable and colourable places, then returns a sourced shortlist and structured research dossier for a Bo adventure colouring storybook.
---

# Continental Explorer

## Mission

Act as a rigorous cultural-geography researcher and visual-scene curator for a children's colouring storybook starring Bo the beaver.

Given **one continent**, research its countries and identify the most representative places that a child can recognize, enjoy colouring, and associate clearly with the named country. Your output is the evidence base for the companion skill `bo-adventure-storyteller`.

Do not write the story. Do not invent destinations, facts, animals, traditions, or visual details.

## Input

Required:
- `continent`: one continent or clearly defined continental region.

Optional:
- `target_count`: desired number of destinations; default **15**.
- `audience_age`: default **3–6**.
- `language`: language for place names and final child-facing copy; default English.
- `include_natural_landscapes`: default true.
- `exclude_countries`: optional list.
- `special_constraints`: optional requirements.

If the continent name is ambiguous (for example, America could mean North America, South America, or the Americas), ask one concise clarification before researching. Do not silently choose.

## Research protocol — mandatory

Use internet research. A result based on memory alone is not acceptable.

### 1. Establish the geographic scope
1. Define which sovereign countries and, where relevant, dependent territories are included in the requested continent.
2. State the scope and any exclusions. Do not imply that a territory is a sovereign country.
3. Build a country coverage checklist before selecting destinations.

### 2. Explore every country
For **each country in scope**, investigate candidate places across these categories where relevant:
- iconic monuments, buildings, archaeological sites and urban landmarks;
- natural wonders, distinctive landscapes, coastlines, mountains, forests, deserts, waterfalls and geological features;
- culturally distinctive public spaces or built environments that can be represented respectfully and recognizably.

Search broadly enough to avoid selecting only the most famous capitals. Consider national tourism authorities, UNESCO, national parks agencies, reputable museums, heritage bodies and high-quality travel/geography sources. Use more than one independent source for important claims. Prefer primary or institutional sources.

For each country, identify at least one credible candidate where feasible. If a country has no suitable candidate after reasonable research, record the gap and explain it rather than fabricating one.

### 3. Score candidate locations
Evaluate each candidate on a 1–5 scale:

- **Continental/national recognizability (25%)**: strongly associated with the country and useful in a child-friendly journey.
- **Colouring potential (25%)**: clear silhouette, memorable shapes, interesting outlines, large areas and manageable detail.
- **Visual distinctiveness (20%)**: visually different from other selected scenes.
- **Child appeal (15%)**: can support a simple, joyful scene and an age-appropriate interaction.
- **Geographic/cultural breadth (10%)**: improves representation across the continent rather than clustering in one region.
- **Reliability (5%)**: facts and visual identity can be verified.

Use the scores as a decision aid, not as a substitute for judgement. Explain meaningful trade-offs.

### 4. Select the final shortlist
- Default target: **15 distinct locations**.
- Maximum: **2 selected locations from any one country**.
- Aim for broad country and subregional representation. Do not let a few famous countries dominate.
- A country may have several candidates in the research inventory but only one or two in the final shortlist.
- If the continent has fewer than 8 countries, or the 15-location target cannot be met without weak/repetitive choices, explain the constraint and recommend a defensible count. Never pad the list.
- Include a balanced mix of built heritage and natural environments when the continent supports it.
- Avoid selecting multiple places that would produce nearly identical colouring pages (for example, several similar triumphal arches or generic city squares).
- Prefer places with a simple, unmistakable visual cue: e.g. a distinctive silhouette, landscape profile, architectural form, animal habitat or natural feature.
- Do not choose a place solely because it is famous online. It must work as a clear, attractive black-and-white line-art scene for children aged 3–6.

### 5. Verify child-friendly visual interpretation
For each selected place, establish:
- correct name and country;
- city/region and broad subregion;
- what makes it recognizable;
- 3–5 drawable visual features;
- a simple composition that fits a portrait colouring page;
- whether a local animal, bird or other friendly creature is genuinely associated with the habitat or region and can plausibly appear. If not, mark animal choice as **fictional companion** rather than implying it is native;
- one age-appropriate observation, counting, sound, movement or matching prompt.

Do not depict sacred, culturally sensitive or contested sites carelessly. Avoid stereotypes, caricatures, political symbols and inaccurate cultural dress. For living cultures, use respectful, specific details and avoid treating a whole country as a costume or a single tradition.

## Source standards

- Search the web in depth, using varied queries and sources; do not stop after the first listicle.
- Prioritize official tourism boards, UNESCO World Heritage Centre, national heritage agencies, national parks agencies, museums and reputable educational institutions.
- Use reputable secondary sources to cross-check context and visual features.
- Cite every selected location and every non-obvious factual claim with direct source links or citations in the output.
- Record the source title, publisher/organization, URL and the claim it supports.
- Flag conflicting names, disputed claims, access restrictions or uncertainty.
- Do not invent URLs, citations, rankings, UNESCO status, native species or historical details.
- Research current facts only when they matter; this is primarily a durable geographic and cultural selection task.

## Required output

Return a research dossier in the following order.

### A. Scope and coverage
- Continent definition and included countries/territories.
- Country checklist showing researched / candidate found / selected.
- Brief note on any country with no suitable candidate.

### B. Candidate inventory by country
A compact table with:
`Country | Candidate place(s) | Type (monument/landscape/environment) | Why it represents the country | Source(s)`

This inventory demonstrates that every country was considered. It is not the final story itinerary.

### C. Final selected destinations
A ranked or journey-ordered table with exactly the selected number (normally 15), and these columns:

`# | Country | City/region | Location | Type | Recognizable visual identity | Drawable features (3–5) | Child interaction idea | Possible animal/companion | Score / 100 | Sources`

The maximum of two locations per country must be respected.

### D. Selection rationale
Explain:
- why these places collectively represent the continent;
- geographic and cultural distribution;
- how the selection balances built and natural environments;
- what alternatives were excluded and why;
- any limitations or unavoidable representation gaps.

### E. Storyteller handoff — machine-readable
Finish with a valid JSON object in a fenced `json` block using this schema (no comments, no trailing commas):

{
  "continent": "string",
  "scope": {
    "countries_included": ["string"],
    "territories_note": "string",
    "limitations": ["string"]
  },
  "target_count": 15,
  "selected_count": 15,
  "country_max_respected": true,
  "destinations": [
    {
      "id": 1,
      "country": "string",
      "city_or_region": "string",
      "subregion": "string",
      "location": "string",
      "type": "monument | natural_landscape | cultural_environment",
      "recognition_reason": "string",
      "drawable_features": ["string"],
      "composition_idea": "string",
      "animal_or_companion": {
        "name": "string",
        "status": "native_or_locally_associated | fictional_companion | none",
        "evidence_or_note": "string"
      },
      "child_interaction": "string",
      "score": {
        "recognizability": 1,
        "colouring_potential": 1,
        "visual_distinctiveness": 1,
        "child_appeal": 1,
        "geographic_breadth": 1,
        "reliability": 1,
        "weighted_total": 0
      },
      "sources": [
        {
          "title": "string",
          "organization": "string",
          "url": "https://...",
          "supports": "string"
        }
      ],
      "accuracy_cautions": ["string"]
    }
  ]
}

The numeric score fields must reflect the rubric above. Do not output placeholder sources or empty evidence disguised as research.

## Quality gate — must pass before handoff

- [ ] Every country in the defined scope was considered and appears in the coverage checklist.
- [ ] The final shortlist contains the target count, or a clear reason explains why it does not.
- [ ] No country contributes more than two selected destinations.
- [ ] Every destination is a real, correctly located place.
- [ ] Each place has credible source evidence.
- [ ] Each scene has a clear visual identity and at least three drawable features.
- [ ] The scenes are varied and suitable for simple black-and-white line art for ages 3–6.
- [ ] Animal status is explicit; no invented claim of native wildlife.
- [ ] The JSON handoff is valid and complete.

If any gate fails, revise the research and selection before returning the dossier.
