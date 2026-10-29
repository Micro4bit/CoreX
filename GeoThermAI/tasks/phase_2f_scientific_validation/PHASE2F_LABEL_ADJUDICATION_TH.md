# Ground Truth & Independent Hydrothermal System Adjudication Protocol

**Scope:** หน่วยวิเคราะห์คือ *independent geothermal system* ที่ผู้เชี่ยวชาญประเมิน ไม่ใช่จำนวนแถวในทะเบียน 47 รายการและไม่ใช่จำนวนจุดน้ำพุร้อน

## Decisions required from expert
1. Review references and coordinates for CR_02/CM_16 and the 31 provisional south points. If unresolvable, preserve `WITHHELD`/`PROVISIONAL` and do not convert to positive training examples.
2. Examine the 18 co-withholding units referenced in Phase 2D for independent hydrothermal system boundaries. A common named location or spatial closeness alone does **not** establish shared reservoir or independence.
3. Assign each evidence record: `VERIFIED_SYSTEM`, `POSSIBLE_SYSTEM`, `SURFACE_MANIFESTATION_ONLY`, or `WITHHELD`, with source and domain explanation; categories below verified must not be implicitly used as ground truth.
4. Assign a stable `system_group_id` only after multidisciplinary review. State evidence for hydrogeologic linkage, relevant faulting and thermal/geochemical evidence, and ambiguous boundaries.
5. Explicitly document whether the label supports hydrothermal manifestation presence, a subsurface reservoir, or electricity-grade geothermal prospectivity. They are different outcomes.
6. Approve the holdout policy and potential detection bias; a listed manifestation is not evidence that an unlisted area is negative.

## Audit / signatures
- Reviewer: name, affiliation, geological expertise, date
- Input registry version SHA-256, row IDs, published sources, geometry/coordinate records and review decision
- Second reviewer for contested boundaries; conflict unresolved -> WITHHOLD
- Approved grouping stored as versioned `adjudication_version`; never mutate original registry

`expert_system_review_template.csv` is intentionally **header only** because no record-level evidence was provided. Copy and populate *from actual repo registry*; do not invent label IDs.

## QC metrics BEFORE model proposal
- Number of unique verified independent system groups **after expert signoff**
- Groups by region and distinct geological play type
- Counts withdrawn / provisional / unresolved, evidence grades, grouping stability
- At least two geographically distinct independent groups in held-out test regions is not itself sufficient: feasibility must be assessed against required model complexity and planned metrics
