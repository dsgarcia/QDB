# Condensation plan for QDB

Source thesis: `Medicion de Credibilidad en Redes Sociales - Final.pdf`

## Core thesis axis

The paper should be framed as a data-quality contribution for social media:
measuring credibility of social media clips through an explicit quality model,
with provenance as a first-class quality signal.

## Best QDB claim

Social media credibility should not be treated only as a prediction problem.
It can be modeled as a data-quality workflow that combines interpretable quality
dimensions, domain-specific metrics, and provenance-aware propagation analysis.

## Main contributions to preserve

- A credibility quality model organized around `Trustworthiness` and
  `Provenance`.
- A decomposition of `Trustworthiness` into `Reputation`, `Verifiability`, and
  `Expertise`.
- An extension of provenance modeling for cross-platform social media sharing.
- The metric `Trustworthiness Path Stability`.
- A modular processing flow for normalized clips, feature generation, quality
  metrics, provenance reconstruction, and final credibility calculation.
- A proof of concept on statin/cholesterol posts validated against a medical
  expert.

## Suggested six-page paper allocation

- Abstract: 0.25 page.
- Introduction: 0.75 page.
- Background and requirements: 0.75 page.
- Credibility quality model: 1.25 pages.
- Provenance-aware flow: 1.25 pages.
- Proof of concept: 1.25 pages.
- Discussion and conclusion: 0.75 page.
- References: included in the six-page limit.

## Likely cuts from the thesis

- Long general background on social media and misinformation.
- Detailed taxonomy of information types.
- Full related-work survey.
- Most implementation details about GCP services.
- Appendices and full JSON schemas.
- Long explanations of each future-work branch.

## Figures and tables to consider

- One compact model diagram replacing thesis Figures 4.1/4.8.
- One compact processing-flow diagram replacing thesis Figures 5.1/7.1.
- One small table with expert vs model results, adapted from Table 7.12.

## Open details

- Confirm final author email and affiliation format.
- Decide whether the submission should be English only or bilingual artifacts for
  local editing.
- Add artifact URL only if the GitHub repositories are intended to be public for
  submission.
