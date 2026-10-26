# Pilot Area Comparison

Date: 2026-10-23  
Decision status: recommendation for a Phase 1 data-engineering pilot, not a final scientific boundary.

## Candidates

| Criterion | Northern corridor: Chiang Mai–Chiang Rai / Fang–Mae Chan–San Kamphaeng context | Southern alternative: Ranong–Phang Nga / Kapong context |
|---|---|---|
| Geological relevance | Published northern study links hot-spring systems to faults and documents named systems. This is source evidence, not proof that a predictor will generalize. | Kapong literature documents a non-volcanic hot-spring case study and fault/fracture context. |
| Verified occurrence evidence | A downloaded GRC paper provides a 16-row hot-spring table with UTM/DMS coordinates; 14 rows have surface temperature. | A public paper/data landing page was located, but a usable regional occurrence inventory was not downloaded in this audit. |
| Predictor coverage | DMR 1:250,000 rock units are queryable; active-fault shapefile was downloaded; one SRTM tile spanning 19–20°N, 98–99°E was inspected. Full structure geometry remains unresolved. | National DMR geological layers can in principle overlap this area. Kapong landing page describes VES/ERT local data, but no raw geophysical files were acquired. |
| Label quality | Better current provenance because the Table 1 coordinates/temperatures were inspected directly. The 16 rows remain spatially clustered and need site grouping. | Promising literature, but label count, exact coordinates, duplicates, and licensing have not been audited from a downloaded source. |
| Spatial separation | Possible only after grouping manifestations into independent systems and mapping their locations. The table contains clusters around named systems; random row splits would leak. | Not currently assessable because an inspected, regional label registry is absent. |
| Licensing/access | DMR active-fault terms conflict and require clarification. Literature data reuse requires citation/permission review. | Mendeley landing page reports CC BY 4.0 for supplemental data, but direct raw data access was not verified; article/table access also remains incomplete. |
| Practical workload | High but bounded: reconcile 16 source points, create site groups, acquire corridor-covering DEM/Landsat, and resolve DMR structure geometry. | Higher initial risk: first acquire and audit labels before meaningful feature engineering. |

## Recommendation

Choose a **conditional Northern Thailand pilot** centered on the verified Fang–Mae Chan–San Kamphaeng/Chiang Mai–Chiang Rai hot-spring evidence, with the actual AOI polygon deferred until label-system grouping is complete.

This recommendation follows observed data access, not presumed geological superiority. The northern source supplies a small but auditable starting registry and published context. It does **not** establish enough independent labels for a robust regional predictive model, and it does not justify a national or commercial-resource claim.

Keep the southern Ranong–Phang Nga / Kapong alternative as the first external-validation candidate, not as an immediate test set. It becomes a defensible comparison only after a downloadable coordinate table is independently audited. The current record of a landing page or an article abstract is insufficient for an external holdout.

## Proposed pilot gate

The pilot proceeds only when all of the following are documented:

1. Northern coordinate reference and site groups are verified from source materials.
2. An AOI is derived from those verified systems, not selected around a desired result.
3. All covariates are available across the AOI with resolution, date, CRS and transformations recorded.
4. At least two candidate spatial/group split designs are tested for feasibility without label-derived features.
5. The number of independent held-out groups is reported before model selection.

If the gate shows too few independent groups, re-scope to an interpretable, nonpredictive evidence-ranking map with sensitivity analysis.

## Sources

- Wood & Singharajwarapan (2014): <https://publications.mygeoenergynow.org/grc/1033597.pdf>
- Ngansom, Pirarai & Duerrast, Kapong supplementary dataset landing page: <https://data.mendeley.com/datasets/37ng92rj85/1>
- Ngansom et al., *Geological setting and hydrogeothermal characteristics of the Kapong non-volcanic hot spring area in Southern Thailand*, DOI <https://doi.org/10.1016/j.geothermics.2019.101746>
- DMR rock units REST: <https://gisportal.dmr.go.th/arcgis/rest/services/GEOL/ROCK_UNIT_250K/MapServer>
