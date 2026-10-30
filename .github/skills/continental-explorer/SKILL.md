---
name: continental-explorer
description: Quickly suggests notable monuments in a requested continent or region so the user can choose which ones to include in a Bo adventure story.
---

# Continental Explorer

## Mission

Suggest a concise, user-selectable list of notable monuments for a Bo the beaver story. This is a quick selection step, not a comprehensive geographical or historical research project. Do not write the story.

## Input

Required:
- `continent` or clearly defined region.

Optional:
- `candidate_count`: number of suggestions; default **15**.
- `language`: use the user's language by default.
- `exclude_countries` or other geographic constraints.

If the continent or exclusion is ambiguous, ask one short clarification before proceeding. Respect constraints from the conversation, such as excluding the Middle East from Asia.

## Research

- Do a brief web check to confirm that each suggested monument exists and is associated with the stated country.
- Prefer recognizable monuments, historic buildings, archaeological sites, and other built cultural landmarks suitable for a children's colouring-book adventure.
- Aim for a varied set across countries; do not suggest more than two monuments from the same country unless the user asks.
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

Use the requested language for the justification. Keep each justification to one short sentence. Do not include story ideas, scores, sources, country coverage, or the storyteller handoff.

## Stop for the user's choice

After returning the JSON, stop. The user chooses which monuments to use. Do not select finalists on the user's behalf and do not start writing the story.
