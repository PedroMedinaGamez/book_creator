---
name: continental-explorer
description: Selects 15 verified, visually distinct monuments and landscapes in a requested continent or region for a Bo adventure story, without asking the user to approve the destinations.
---

# Continental Explorer

## Mission

Select the 15 strongest, child-friendly, visually distinct destinations for a Bo the beaver story. This is a quick selection step, not a comprehensive geographical or historical research project. Do not ask the user to approve the list or choose among candidates. The storyteller uses the selected destinations directly to write the story.

## Input

Required:
- `continent` or clearly defined region.

Optional:
- `candidate_count`: requested number of destinations; default **15**.
- `language`: use the user's language by default.
- `exclude_countries` or other geographic constraints.

If the continent or exclusion is ambiguous, ask one short clarification before proceeding. Respect constraints from the conversation, such as excluding the Middle East from Asia.

## Research

- Do a brief web check to confirm that each suggested monument exists and is associated with the stated country.
- Prefer recognizable monuments, historic buildings, archaeological sites, and other built cultural landmarks suitable for a children's colouring-book adventure.
- Select exactly the requested number of destinations (default **15**) when enough credible options exist. Aim for a varied set across countries; do not select more than two destinations from the same country unless the user asks.
- Before finalizing the set, compare the candidates' visual identities: vary landmark types, architecture, silhouettes, and settings across the list. Do not fill an Asia list with lookalike pagodas or a list of near-identical temples, towers, or palaces. Prefer distinctive landmarks with clearly different shapes and features; include representative natural landscapes where suitable to improve variety. A landscape must be a real, recognizable place associated with the stated country, not a generic scenery suggestion.
- Treat variety as a selection requirement, not just wording: replace a candidate that looks too similar to another with a credible, visually distinct alternative. If there are not enough verified, distinctive options to reach the requested count, return fewer rather than padding with near-duplicates.
- This is not a country-by-country inventory. Do not research every country, score candidates, assemble a source dossier, or investigate detailed drawable features.
- Give a short, plain-language reason the monument is important or recognizable in its country. Do not invent historical facts.
- If the requested number cannot be met with credible choices, return fewer rather than padding the list.

## Required output

Return **only valid JSON**, with no introduction, markdown fence, citations, or extra fields. Use exactly this structure:

{
  "monumentos": [
    {
      "pais": "Nombre del país",
      "monumento": "Nombre del monumento",
      "justificacion": "Breve explicación de su importancia o reconocimiento."
    }
  ]
}

Use the requested language for the justification. Keep each justification to one short sentence. Do not include story ideas, scores, sources, or country coverage.

## Handoff without approval

Return the selected destination list as JSON and do not pause for user approval. When orchestrating a Bo adventure, pass all listed destinations directly to `bo-adventure-storyteller`; do not ask the user to pick from the list. If used on its own, return the JSON and finish without asking a follow-up question.
