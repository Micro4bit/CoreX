# GeoThermAI — Project Master

Version: 0.2 | Updated: 2026-10-23 | Owner: Human project owner | Status: Core Idea LOCKED; research viability CONDITIONALLY PASSED pending labels/validation.

## North star
GeoThermAI is a Thailand-focused, uncertainty-aware geospatial decision-support research project to prioritize follow-up geothermal exploration. Its primary contribution is not automatic discovery of commercial reservoirs: it is scientifically evaluated exploration screening and ranking under data constraints.

## Competition
Track 3: Digital Energy Transition. Shared judging rubric recorded by project: economic/social/environmental benefit 35; scientific feasibility/application 30; novelty 20; presentation video 10; team 5. Exact organizer documentation should be retained when available.

## The problem and defensible impact
Geothermal exploration requires costly decisions while subsurface observations are sparse. Thai geology, structural geology, hot springs and satellite information exist in different formats. Better screening could help choose which areas deserve expensive fieldwork. **Potential impact** is better allocation of exploration effort; no monetary reduction, MW, discovered resources, LCOE, or drilling success has been proved.

## Core research questions
1. Do combined geospatial predictors outperform a transparent geological screening baseline in spatially held-out evaluation?
2. Do satellite-derived features provide independent signal beyond geology and structural data?
3. Do complex models generalize better than interpretable Logistic Regression / simpler alternatives?
4. Do uncertainty-aware rankings help under explicit hypothetical survey-budget constraints?

## Locked research direction
- Geographic relevance: Thailand, with a pilot area selected by measurable data sufficiency.
- Main product: prospectivity screening map + evidence/uncertainty map + defensible validation + prioritized exploration candidates.
- Scientific approach: baseline-first, spatial validation, ablation, provenance, reporting of negative findings.
- Satellite fusion: test as a hypothesis, not assumed useful.
- Economic screening: scenario module, not bankable site economics.
- PDP/data-center story: optional contextual application only, with official verification.

## Not locked
Pilot boundaries; labels; dataset permissions; exact grid and map scale; model choice; confidence calibration; economic parameters; final impact claims.

## Hard distinctions
- Hot spring occurrence ≠ commercially viable reservoir.
- No known occurrence ≠ negative observation.
- Satellite land surface temperature ≠ deep-reservoir temperature.
- Prospectivity score ≠ resource MW, success probability, or validated LCOE.
- Map display ≠ successful AI model.

## MVP acceptance tests
- At least one pilot area and documented source-to-variable provenance.
- Reproducible geological/rule baseline and a simple ML baseline.
- Leakage audit + spatially held-out testing.
- Satellite ablation comparison.
- Transparent sample counts, suitable evaluation measures and uncertainty limitations.
- Honest map with uncertainty / poor-evidence regions.
- Comparison of exploration selection policies only under identified simulated assumptions.

## Status following Data Feasibility Audit 1
**Conditional GO for data engineering and a pilot evaluation; NO-GO for claims of validated geothermal AI prospectivity until independent labels and feasible geographic validation exist.** See 02 Research and 03 Agent Context.

## Change control
Human owner has final authority. All model-proposed changes to locked objectives must be submitted as a change request and explicitly approved. The Master AI Coordinator prepares task-specific prompts, checks deliverables and exposes uncertainty, but is not an independent authority to alter the research objective.
