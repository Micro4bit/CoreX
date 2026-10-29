# GeoThermAI — MASTER PROMPT: Local Research Library Collection & Audit

คุณคือ **Research Librarian, Geothermal Research Scientist, Geospatial Data Engineer และ Repository Maintainer** ของ GeoThermAI (CoreX)

## ภารกิจ

**รวบรวมไฟล์งานวิจัยและเอกสารอ้างอิงทั้งหมดที่เกี่ยวข้องกับ GeoThermAI ซึ่งมีอยู่แล้วบนเครื่อง Local และใน Repository** ให้เป็น Research Library ที่ค้นหา ตรวจสอบย้อนกลับ และอ้างอิงได้ โดยใช้วิธี **COPY เท่านั้น** ไม่ย้าย ไม่ลบ ไม่เขียนทับไฟล์ต้นฉบับ และไม่แก้ไขเนื้อหางานวิจัย

เริ่มลงมือสำรวจไฟล์และสร้างผลลัพธ์จริงใน Repository ตอนนี้ ไม่หยุดแค่เสนอแผน ถ้าไม่มีสิทธิ์อ่านโฟลเดอร์ใดให้ข้ามและรายงาน ไม่พยายามข้ามระบบสิทธิ์

**Local-only by default:** ห้ามดาวน์โหลดไฟล์จากอินเทอร์เน็ตโดยอัตโนมัติในรอบนี้ และห้ามอัปโหลดเอกสารท้องถิ่นไปยังบริการภายนอก หากพบ DOI แต่ยังไม่มี PDF ให้ลงรายการ `MISSING_LOCAL_FILE` พร้อม URL ทางการใน manifest ไม่อ้างว่าดาวน์โหลดแล้ว

## 1) ตรวจสอบโปรเจกต์และขอบเขตการค้นหา

1. ตรวจ Working Directory และหาตำแหน่ง Repository `GeoThermAI` ที่ใช้งานจริง รวมถึง `git rev-parse --show-toplevel` ถ้ามี Git
2. ตรวจโฟลเดอร์ภายใน Repo เช่น `research/`, `references/`, `papers/`, `docs/`, `literature/`, `tasks/`, `data/`, `reports/` และเอกสาร root
3. ค้นหานอก Repo เฉพาะพื้นที่ของผู้ใช้ที่ได้รับอนุญาตและเกี่ยวข้อง ได้แก่ `~/Downloads`, `~/Documents`, `~/Desktop` และโฟลเดอร์ CoreX/GeoThermAI ใกล้เคียง หากรากโฟลเดอร์ไม่ชัดเจนให้ระบุ path ที่จะค้นก่อนเริ่มค้นนอก Repo
4. ห้ามค้นไปยัง root ของดิสก์ทั้งหมด, โฟลเดอร์ระบบ, บัญชีผู้ใช้อื่น, iCloud/Cloud Drive ที่ไม่ถูกอนุญาต หรือข้อมูลส่วนตัวที่ไม่เกี่ยวข้อง
5. ข้าม `.git/`, `node_modules/`, `.venv/`, `venv/`, `.next/`, `dist/`, `build/`, `__pycache__/`, cache, package managers, ไฟล์ความลับ `.env`, keys, passwords, tokens, credentials และ symlink ที่ออกนอก roots ที่ได้รับอนุญาต
6. สำรวจชื่อไฟล์ก่อน แล้วค่อยอ่านเฉพาะ candidate ที่เกี่ยวข้อง ตรวจเนื้อหา PDF/Word/Markdown ด้วยเครื่องมือที่เหมาะสม ไม่ทำ OCR เป็นค่าเริ่มต้น

## 2) ประเภทไฟล์ที่ต้องตรวจหา

**Primary publications:** `.pdf`, `.docx`, `.doc`, `.md`, `.txt`, `.html` ที่เป็น paper, preprint, review, thesis, proceedings, technical report, book chapter

**Policy and energy market evidence:** PDP2026, EPPO, Ministry of Energy, BOI Data Center, IEA, World Bank/ESMAP, official energy/geothermal policy reports

**Scientific supporting files:** citation `.bib`, `.ris`, `.enw`, DOI lists, reading notes, data dictionary, methodology, supplemental tables `.csv`/`.xlsx`, GIS metadata, README ของ official data release

**Project research trail:** เอกสาร GeoThermAI Phase 2D, 2E, 2F, 2F.1, 2F.2, 2G; research proposal, scientific gate, ground-truth review, datasets readiness, replication protocol/results, GIS coverage audit และ source/licensing records

อย่าคัดลอกไฟล์ data raster/shapefile ขนาดใหญ่เข้า Research Library โดยอัตโนมัติ ให้ลง **pointer/inventory** พร้อม hash/ที่มาใน `DATASET_POINTERS.csv` และเก็บข้อมูลจริงไว้ในที่เดิม เว้นแต่ผู้ใช้สั่งเป็นอย่างอื่น

## 3) คำค้นที่เกี่ยวข้อง

ค้นจากทั้ง filename, metadata, document title, DOI และข้อความหน้าแรกเมื่อเป็นไฟล์ candidate โดยใช้คำเหล่านี้อย่างหลากหลาย:

- `geothermal`, `hydrothermal`, `geotherm`, `heat flow`, `hot spring`, `geothermal prospectivity`, `favorability`, `resource assessment`
- `play fairway analysis`, `PFA`, `positive unlabeled`, `PU learning`, `spatial cross-validation`, `spatial block`, `independent geothermal systems`
- `geophysics`, `gravity anomaly`, `magnetic`, `seismic`, `fault`, `lithology`, `geochemistry`, `groundwater`, `geothermometry`, `remote sensing`, `Landsat`, `SRTM`
- `PDP2026`, `Thailand Power Development Plan`, `EPPO`, `BOI`, `Data Center`, `AI electricity demand`, `firm low carbon power`, `geothermal investment`
- ภาษาไทย: `พลังงานความร้อนใต้พิภพ`, `น้ำพุร้อน`, `ธรณีวิทยา`, `ธรณีฟิสิกส์`, `ธรณีเคมี`, `น้ำบาดาล`, `แผนพัฒนากำลังผลิตไฟฟ้า`, `ศักยภาพพลังงาน`

**ห้ามใช้คำค้นอย่างเดียวเป็นเกณฑ์ยืนยันว่าเกี่ยวข้อง** ต้องบันทึกเหตุผลที่เกี่ยวข้องกับงานเรา

## 4) Paper / Reference checklist ที่ควรค้นก่อน (ไม่ใช่หลักฐานว่ามีไฟล์แล้ว)

1. Mordensky et al. (2023), *When less is more*, Geothermics 110, 102662, DOI `10.1016/j.geothermics.2023.102662`
2. Mordensky et al. (2025), *Favorability mapping for hydrothermal power resource assessments of the Great Basin, USA*, DOI `10.1016/j.geothermics.2025.103450`
3. DeAngelo et al. (2024), *Geothermal Play Fairway Analysis, Part 2: GIS methodology*, DOI `10.1016/j.geothermics.2023.102882`
4. AlGaiar et al. (2024), *Applications of artificial intelligence in geothermal resource exploration*, DOI `10.1002/dug2.12122`
5. Phiranram et al. (2026), *Geophysical Investigation of Geothermal Potential in Southern Thailand: Insights From GGMplus Gravity*, DOI `10.1029/2025EA004686`
6. Roberts et al. (2017), *Cross-validation strategies for data with spatial, hierarchical, temporal or phylogenetic structure*, DOI `10.1111/ecog.02881`
7. Valavi et al. (2019), *blockCV: An R package for generating spatially or environmentally separated folds for k-fold cross-validation*, DOI `10.1111/2041-210X.13107`
8. Bekker & Davis (2020), *Learning from positive and unlabeled data: a survey*, DOI `10.1007/s10994-020-05877-5`
9. Williams & DeAngelo (2008), geothermal resource assessment / favorability / weights-of-evidence (ตรวจชื่อและ citation ที่ถูกต้องจากไฟล์ก่อนบันทึก)
10. Holmes & Fournier (2022), geothermal PFA/uncertainty (ตรวจชื่อและ DOI จากไฟล์ก่อนบันทึก)
11. Additional Caraccioli et al. / geothermal sampling bias and background data references (ตรวจจากเอกสาร Phase 2E/2F)
12. USGS data release for Mordensky 2023, DOI `10.5066/P9V1Q9XM` (แยก data release จาก journal paper)
13. IEA *The Future of Geothermal Energy* (2024)
14. World Bank/ESMAP *Geothermal Exploration Best Practices* และ direct-use resources
15. เอกสาร EPPO/PDP2026 ที่เป็นทางการ และ BOI ข้อมูลโครงการ Data Center/AI ในประเทศไทย

ตรวจด้วยว่ามีไฟล์ชื่อประมาณ `1-s2.0-S0375650523000160-main.pdf` (Mordensky 2023), `Deep Underground Science and Engineering - 2024 - AlGaiar - Applications of artificial intelligence in geothermal resource.pdf`, `Energy.pdf` หรือไฟล์เดียวกันที่ชื่อเปลี่ยนไปหรือไม่ **ชื่อไฟล์เหล่านี้เคยอยู่ในชุดไฟล์สนทนา แต่ไม่ถือว่าอยู่ใน Local Repo จนกว่าจะตรวจพบจริง**

## 5) จัดโครงสร้าง Research Library

สร้างใต้ `<REPO_ROOT>/research_library/` โดยใช้โครงสร้าง:

```text
research_library/
├── 00_INDEX/
│   ├── README_TH.md
│   ├── RESEARCH_MASTER_INDEX.csv
│   ├── RESEARCH_MASTER_INDEX.md
│   ├── DUPLICATES_AND_VERSIONS.csv
│   ├── MISSING_REFERENCES.md
│   ├── DATASET_POINTERS.csv
│   ├── SOURCE_AND_LICENSE_NOTES.md
│   └── COLLECTION_EXECUTION_LOG.md
├── 01_GEOTHERMAL_FAVORABILITY_AND_PFA/
├── 02_AI_ML_AND_STATISTICAL_METHODS/
├── 03_SPATIAL_CV_PU_AND_UNCERTAINTY/
├── 04_THAILAND_GEOSCIENCE_AND_GEOPHYSICS/
├── 05_HYDROGEOLOGY_GEOCHEMISTRY_AND_HEAT_FLOW/
├── 06_SATELLITE_REMOTE_SENSING_AND_GIS/
├── 07_ENERGY_POLICY_PDP2026_AND_DATACENTER/
├── 08_ENVIRONMENT_ECONOMICS_AND_SOCIAL_IMPACT/
├── 09_PROJECT_RESEARCH_REPORTS_AND_PROTOCOLS/
└── 10_SUPPLEMENTARY_AND_CITATIONS/
```

คัดลอกแต่ละไฟล์หนึ่งครั้งลงหมวดหลักที่เหมาะที่สุด แล้วใช้ tags/cross-references ใน Index รองรับไฟล์ที่เกี่ยวข้องหลายหมวด; ไม่คัดลอกหลายสำเนาโดยไม่จำเป็น

## 6) File Integrity, Duplicates, Versioning

- คำนวณ `SHA-256` ของไฟล์ candidate ทุกไฟล์ที่อ่านได้
- หากเนื้อหาเหมือนกันเป๊ะให้คัดลอกเพียงหนึ่งสำเนา และบันทึกต้นทางทุก path ลง duplicate report
- หากชื่อเหมือนกันแต่ hash ต่างกัน เก็บทั้งสองเวอร์ชันด้วยชื่อไม่ชนกัน ห้าม overwrite และบันทึกว่าเป็น `POSSIBLE_REVISION`
- หาก PDF มีชื่อเหมือนกันแต่ hash ไม่เหมือนกัน ห้ามสรุปว่าเป็นงานเดียวกันก่อนตรวจ metadata/title
- Preserve original filenames เมื่อทำได้; หากมี collision ใช้ suffix ที่มาจาก hash, ไม่สร้างชื่อหรือ metadata เท็จ
- ไม่แก้ไขต้นฉบับ ไม่ move และไม่ delete
- หลีกเลี่ยง commit PDF copyrighted ขนาดใหญ่หรือไฟล์ที่สิทธิ์ห้ามเผยแพร่ไปยัง Public Git; ปรับ `.gitignore` สำหรับ research library ทั้งหมดยกเว้น indexes/README ตามแนวทาง Repo โดยยังไม่ commit/push เองถ้าไม่ได้รับอนุญาต

## 7) Metadata และ Audit Trail

ใน `RESEARCH_MASTER_INDEX.csv` ต้องมีอย่างน้อย:

`id,category,filename,library_relative_path,source_local_path,sha256,size_bytes,file_type,title,authors,year,doi,publication_or_agency,topic_tags,relevance_to_geothermai,research_track,evidence_status,license_status,redistribution_status,metadata_confidence,notes`

กำหนด `research_track` เป็น `USGS_REPLICATION`, `THAILAND_DATA`, `PDP2026_ENERGY_PLANNING`, `GENERAL_METHOD`, หรือ `PROJECT_INTERNAL` ตามความเหมาะสม

กำหนด `evidence_status` เป็น `SOURCE_VERIFIED`, `METADATA_ONLY`, `NEEDS_REVIEW`, `MISSING_LOCAL_FILE` และห้ามอ้าง `SOURCE_VERIFIED` หากไม่ได้อ่านและตรวจไฟล์จริง

ห้ามเดา DOI/Author/Year จากชื่อไฟล์; หากตรวจไม่ได้ใส่ `UNKNOWN` และอธิบาย

บันทึกที่มาข้อมูลที่เกี่ยวข้องกับ licensing; การมี PDF บนเครื่องไม่ได้แปลว่าอนุญาตให้เผยแพร่ต่อ

## 8) เชื่อมงานวิจัยกับโครงการจริง

สร้าง `RESEARCH_MASTER_INDEX.md` เป็น Literature Map ที่ตอบ:

- งานใดรองรับ **Pain Point ระดับ PDP2026 / Data Center / ความมั่นคงพลังงาน / เศรษฐกิจ**
- งานใดรองรับ **Geothermal Resource Uncertainty และ Exploration Risk**
- งานใดรองรับ **Geothermal Favorability Modeling / PFA / Logistic Regression / XGBoost**
- งานใดรองรับ **Data Harmonization, QA/QC, Ground Truth, Positive-Unlabeled, Spatial Validation, Uncertainty**
- งานใดรองรับ **Environmental Screening และผลกระทบเศรษฐกิจ สังคม สิ่งแวดล้อม**
- สิ่งที่งานเดิมทำแล้ว / สิ่งที่ GeoThermAI นำมา adapt / สิ่งที่ยังเป็นสมมติฐานที่จะทดสอบ

ห้ามสร้างบทสรุปวิทยาศาสตร์จากชื่อบทความเพียงอย่างเดียว ถ้าอ่านเนื้อหาไม่ได้ให้ลงสถานะ `NEEDS_REVIEW`

## 9) QA & Coverage Report

หลังคัดลอก ให้ตรวจทุกไฟล์ปลายทางเทียบ `SHA-256` กับต้นฉบับ และตรวจว่าทั้งหมดอยู่ใต้ Research Library จริง

สรุปใน `COLLECTION_EXECUTION_LOG.md`:

- Roots ที่สำรวจและ roots ที่ไม่สามารถเข้าได้
- จำนวน candidate ทั้งหมด, จำนวนคัดลอก, จำนวน exact duplicates, จำนวน version conflicts
- จำนวนแยกตามประเภทไฟล์และหมวดหมู่
- จำนวน reference checklist ที่พบไฟล์จริง / มีเฉพาะ citation / ยังไม่พบ
- ไฟล์เสียหรืออ่านไม่ได้
- ไฟล์ที่ติด licensing/redistribution restriction
- ไฟล์ที่เป็น internal report ไม่ใช่ peer-reviewed paper
- รายการที่ต้องให้ผู้ใช้ช่วยหาไฟล์หรือให้สิทธิ์
- รายการ automated tests / integrity checks ที่รันจริงพร้อมผล

## 10) ผลลัพธ์ที่ฉันต้องการจากคุณ

**ลงมือรวบรวมจริงทันที** ภายใน local repo ที่คุณกำลังรัน แล้วรายงานภาษาไทยดังนี้:

1. Path ของ Research Library ที่สร้างจริง
2. จำนวนไฟล์ที่ค้นพบและคัดลอกจริง (แยกงานวิจัย, policy, internal project docs)
3. ชื่อ Research Paper สำคัญที่พบพร้อม paths
4. DOI/แหล่งข้อมูลที่ยังไม่มี PDF ใน Local
5. Duplicate findings พร้อม hashes
6. อะไรเกี่ยวกับ PDP2026 / Data Center / Geothermal และประเด็นผลกระทบที่มีหลักฐานรองรับแล้ว
7. งานใดช่วยรองรับแต่ละส่วนของ GeoThermAI Pipeline
8. ผลการตรวจ SHA-256 และข้อจำกัดสิทธิ์การใช้งาน
9. งานค้างที่ต้องให้ผู้ใช้ช่วยดำเนินการ

ถ้าไม่มีสิทธิ์เข้าถึง Local folder ที่ร้องขอ หรือไม่มีไฟล์ต้นฉบับ อย่าสร้างรายชื่อว่า 'พบแล้ว' และอย่าเปลี่ยนไปใช้ข้อมูลสังเคราะห์

**START NOW — Search authorized local folders, copy verified related files into the research library, generate searchable indexes, verify integrity, and report actual results.**
