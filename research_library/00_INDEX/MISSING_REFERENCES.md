# GeoThermAI — Audit of Missing Local References and Acquisition Roadmap

> **Data Stewardship & Scientific Integrity Directive**:
> สถานะ `MISSING_LOCAL_FILE` แสดงว่าบทความนี้เป็น **เอกสารเป้าหมายหลัก (Target Reference)** ที่สำคัญอย่างยิ่งต่อระเบียบวิธีวิจัย แต่ยังไม่มีไฟล์ PDF/ต้นฉบับฉบับเต็มอยู่บนระบบจัดเก็บข้อมูล Local ของผู้ใช้
> ห้ามสร้างข้ออ้างว่าดาวน์โหลดแล้ว และห้ามสร้างผลลัพธ์โมเดลโดยอ้างว่าอ่านข้อมูลฉบับเต็มแล้วจนกว่าจะได้ไฟล์จริงมาเปิดและคำนวณ SHA-256

---

## 1. ตารางสรุปสถานะเอกสารเป้าหมาย (Checklist R01 – R12)

| Ref ID | Lead Author / Agency | Year | Short Title | Official DOI / URL | Local Status | Primary Category |
|---|---|---:|---|---|---|---|
| **R01** | Mordensky et al. | 2023 | When less is more: Data pruning and feature selection | [10.1016/j.geothermics.2023.102662](https://doi.org/10.1016/j.geothermics.2023.102662) | `MISSING_LOCAL_FILE` | `01_GEOTHERMAL_FAVORABILITY_AND_PFA` |
| **R02** | Mordensky et al. | 2025 | Favorability mapping for hydrothermal power resource assessments | [10.1016/j.geothermics.2025.103450](https://doi.org/10.1016/j.geothermics.2025.103450) | `MISSING_LOCAL_FILE` | `01_GEOTHERMAL_FAVORABILITY_AND_PFA` |
| **R03** | DeAngelo et al. | 2024 | Geothermal Play Fairway Analysis Part 2 GIS methodology | [10.1016/j.geothermics.2023.102882](https://doi.org/10.1016/j.geothermics.2023.102882) | `MISSING_LOCAL_FILE` | `01_GEOTHERMAL_FAVORABILITY_AND_PFA` |
| **R04** | AlGaiar et al. | 2024 | Applications of artificial intelligence in geothermal resource exploration | [10.1002/dug2.12122](https://doi.org/10.1002/dug2.12122) | `MISSING_LOCAL_FILE` | `02_AI_ML_AND_STATISTICAL_METHODS` |
| **R05** | Phiranram et al. | 2026 | Geophysical Investigation in Southern Thailand (GGMplus Gravity) | [10.1029/2025EA004686](https://doi.org/10.1029/2025EA004686) | `MISSING_LOCAL_FILE` | `04_THAILAND_GEOSCIENCE_AND_GEOPHYSICS` |
| **R06** | Roberts et al. | 2017 | Cross-validation strategies for data with spatial structure | [10.1111/ecog.02881](https://doi.org/10.1111/ecog.02881) | `MISSING_LOCAL_FILE` | `03_SPATIAL_CV_PU_AND_UNCERTAINTY` |
| **R07** | Valavi et al. | 2019 | blockCV: Spatially or environmentally separated folds | [10.1111/2041-210X.13107](https://doi.org/10.1111/2041-210X.13107) | `MISSING_LOCAL_FILE` | `03_SPATIAL_CV_PU_AND_UNCERTAINTY` |
| **R08** | Bekker & Davis | 2020 | Learning from positive and unlabeled data: a survey | [10.1007/s10994-020-05877-5](https://doi.org/10.1007/s10994-020-05877-5) | `MISSING_LOCAL_FILE` | `03_SPATIAL_CV_PU_AND_UNCERTAINTY` |
| **R09** | USGS | 2023 | USGS Data Release for Mordensky 2023 | [10.5066/P9V1Q9XM](https://doi.org/10.5066/P9V1Q9XM) | `SOURCE_VERIFIED` | `10_SUPPLEMENTARY_AND_CITATIONS` |
| **R10** | IEA | 2024 | The Future of Geothermal Energy | [IEA Report URL](https://www.iea.org/reports/the-future-of-geothermal-energy) | `METADATA_ONLY` | `07_ENERGY_POLICY_PDP2026_AND_DATACENTER` |
| **R11** | EPPO | 2026 | Thailand Draft PDP2026 Official Documentation | [EPPO Official Portal](https://www.eppo.go.th/) | `METADATA_ONLY` | `07_ENERGY_POLICY_PDP2026_AND_DATACENTER` |
| **R12** | BOI | 2026 | Thailand Data Center & AI Investment Policies | [BOI Official Portal](https://www.boi.go.th/) | `METADATA_ONLY` | `07_ENERGY_POLICY_PDP2026_AND_DATACENTER` |

---

## 2. รายละเอียดและความสำคัญของแต่ละเอกสารต่อ GeoThermAI

### R01: Mordensky et al. (2023)
- **ชื่อเต็ม**: *When less is more: How data pruning and feature selection improve machine learning models for geothermal favorability*
- **วารสาร**: *Geothermics*, Volume 110, 102662.
- **DOI**: `10.1016/j.geothermics.2023.102662`
- **บทบาทต่อโครงการ**: เป็น **Primary Algorithmic Baseline** ของโครงการ โดยแสดงให้เห็นว่าการคัดกรองตัวแปร (feature pruning) และการจัดการกับ Positive-Unlabeled (PU) regime ช่วยเพิ่มความแม่นยำของโมเดลความน่าจะเป็นและลด false positives อย่างมีนัยสำคัญ
- **สิ่งที่รอการยืนยันจากไฟล์จริง**: รายการตัวแปรทางธรณีฟิสิกส์ 21 ตัวแปรฉบับเต็ม, สูตรสมการ loss weighting, และสถิติ hyperparameter tuning ดั้งเดิม

### R02: Mordensky et al. (2025)
- **ชื่อเต็ม**: *Favorability mapping for hydrothermal power resource assessments of the Great Basin, USA*
- **วารสาร**: *Geothermics*, Volume 124, 103450.
- **DOI**: `10.1016/j.geothermics.2025.103450`
- **บทบาทต่อโครงการ**: ต่อยอดการประเมินศักยภาพความร้อนใต้พิภพด้วย Monte Carlo uncertainty analysis และการนำหลักฐานหลุมเจาะ (ordinal well evidence) เข้ามาร่วมคำนวณ
- **สิ่งที่รอการยืนยันจากไฟล์จริง**: การคำนวณช่วงความเชื่อมั่น (confidence intervals) และการกระจายตัวของความไม่แน่นอนเชิงพื้นที่

### R03: DeAngelo et al. (2024)
- **ชื่อเต็ม**: *Geothermal Play Fairway Analysis, Part 2: GIS methodology*
- **วารสาร**: *Geothermics*, Volume 116, 102882.
- **DOI**: `10.1016/j.geothermics.2023.102882`
- **บทบาทต่อโครงการ**: เป็นระเบียบวิธี Play Fairway Analysis (PFA) เชิงพื้นที่มาตรฐานสากล สำหรับการรวมชั้นข้อมูล Heat Engine, Permeability, และ Seal เข้าด้วยกัน
- **สิ่งที่รอการยืนยันจากไฟล์จริง**: น้ำหนักของชั้นข้อมูลโครงสร้างรอยเลื่อนและ spatial kernel density parameters

### R04: AlGaiar et al. (2024)
- **ชื่อเต็ม**: *Applications of artificial intelligence in geothermal resource exploration*
- **วารสาร**: *Deep Underground Science and Engineering*, Wiley.
- **DOI**: `10.1002/dug2.12122`
- **บทบาทต่อโครงการ**: บทความทบทวนวรรณกรรมระดับโลก (comprehensive review) เกี่ยวกับการประยุกต์ใช้ AI/ML (Random Forest, SVM, Deep Learning, XGBoost) ในการสำรวจความร้อนใต้พิภพ
- **สิ่งที่รอการยืนยันจากไฟล์จริง**: Benchmark comparison matrix และ failure modes ที่พบบ่อยในธรณีวิทยาเอเชีย

### R05: Phiranram et al. (2026)
- **ชื่อเต็ม**: *Geophysical Investigation of Geothermal Potential in Southern Thailand: Insights From GGMplus Gravity*
- **วารสาร**: *Earth and Space Science*, AGU / Wiley.
- **DOI**: `10.1029/2025EA004686`
- **บทบาทต่อโครงการ**: เป็นงานวิจัยธรณีฟิสิกส์ล่าสุดที่ใช้ข้อมูลความผิดปกติของแรงโน้มถ่วง GGMplus (Gravity Anomaly) ประเมินโครงสร้างความร้อนใต้พิภพในภาคใต้ของประเทศไทย
- **สิ่งที่รอการยืนยันจากไฟล์จริง**: พิกัดจุด anomaly, ค่า residual gravity Bouguer, และการเชื่อมโยงกับแนวรอยเลื่อนระนอง-คลองท่อม

### R06: Roberts et al. (2017)
- **ชื่อเต็ม**: *Cross-validation strategies for data with spatial, hierarchical, temporal or phylogenetic structure*
- **วารสาร**: *Ecography*, 40(8), 913-929.
- **DOI**: `10.1111/ecog.02881`
- **บทบาทต่อโครงการ**: ทฤษฎีหลักการทำ Spatial Cross-Validation เพื่อป้องกัน data leakage จาก spatial autocorrelation ในข้อมูลเชิงพื้นที่
- **สิ่งที่รอการยืนยันจากไฟล์จริง**: สูตรคำนวณ effective sample size และ spatial block radius selection criteria

### R07: Valavi et al. (2019)
- **ชื่อเต็ม**: *blockCV: An R package for generating spatially or environmentally separated folds for k-fold cross-validation*
- **วารสาร**: *Methods in Ecology and Evolution*, 10(2), 225-232.
- **DOI**: `10.1111/2041-210X.13107`
- **บทบาทต่อโครงการ**: อัลกอริทึมการแบ่งกลุ่มข้อมูลทดสอบเชิงพื้นที่ (spatial blocking folds) ที่ GeoThermAI นำมาแปลงเป็น Python implementation
- **สิ่งที่รอการยืนยันจากไฟล์จริง**: การวิเคราะห์ semi-variogram เพื่อกำหนดขนาด spatial block อัตโนมัติ

### R08: Bekker & Davis (2020)
- **ชื่อเต็ม**: *Learning from positive and unlabeled data: a survey*
- **วารสาร**: *Machine Learning*, 109, 719-760.
- **DOI**: `10.1007/s10994-020-05877-5`
- **บทบาทต่อโครงการ**: ทฤษฎีบทการเรียนรู้แบบ Positive-Unlabeled (PU Learning) ภายใต้สมมติฐาน SCAR (Selected Completely At Random) และ SAR (Selected At Random)
- **สิ่งที่รอการยืนยันจากไฟล์จริง**: Risk estimator formulations และ propensity score estimation methods

### R10: IEA (2024)
- **ชื่อเต็ม**: *The Future of Geothermal Energy*
- **องค์กร**: International Energy Agency (IEA), Paris.
- **URL**: `https://www.iea.org/reports/the-future-of-geothermal-energy`
- **สถานะ**: `METADATA_ONLY` (สาระสำคัญและตัวเลขต้นทุน LCOE ถูกบันทึกไว้ใน `PHASE2G_PDP2026_DATACENTER_EVIDENCE_TH.md` แล้ว แต่ยังไม่มีตัวเล่มรายงานฉบับเต็ม PDF ในเครื่อง)

### R11: EPPO (2026)
- **ชื่อเต็ม**: *Thailand Draft Power Development Plan 2024-2037 (PDP2026)*
- **องค์กร**: สำนักงานนโยบายและแผนพลังงาน (สนพ. / EPPO), กระทรวงพลังงาน.
- **URL**: `https://www.eppo.go.th/`
- **สถานะ**: `METADATA_ONLY` (ตัวเลขเป้าหมายพลังงานหมุนเวียน 51% และการจัดสรร Direct PPA ของ Data Center ถูกสังเคราะห์ไว้ในเอกสาร Phase 2G)

### R12: BOI (2026)
- **ชื่อเต็ม**: *Data Center and Cloud Services AI Investment Promotion Announcements*
- **องค์กร**: สำนักงานคณะกรรมการส่งเสริมการลงทุน (BOI).
- **URL**: `https://www.boi.go.th/`
- **สถานะ**: `METADATA_ONLY` (ข้อมูลการลงทุนกว่า 1.6 แสนล้านบาทและข้อกำหนดไฟฟ้า Clean Baseload ถูกสรุปไว้ในระบบ)

---

## 3. เอกสารอื่นที่ต้องค้นหาเพิ่มเติม (Additional Literature)
1. **Williams & DeAngelo (2008)**: Geothermal resource assessment / favorability / weights-of-evidence (USGS Circular 1363).
2. **Holmes & Fournier (2022)**: Geothermal PFA and geothermometry uncertainty modeling.
3. **Caraccioli et al.**: Geothermal sampling bias and background selection strategies.

---

## 4. แผนงานการจัดหาเอกสารสำหรับผู้ใช้ (Acquisition Protocol)
1. **ห้ามใช้ Web Scraping อัตโนมัติ**: การใช้ Agent ดูดไฟล์ที่มีลิขสิทธิ์จากฐานข้อมูลวารสารโดยไม่ผ่านการยืนยันตัวตนผิดข้อตกลงการใช้งานและอาจถูกบล็อก IP
2. **ช่องทางการขอรับสิทธิ์เข้าถึงอย่างถูกกฎหมาย**:
   - เข้าถึงผ่านระบบห้องสมุดมหาวิทยาลัยหรือสถาบันวิจัยของผู้ใช้ (Institutional Access / EZproxy / OpenAthens)
   - เข้าถึงคลัง Open Access หรือ Green OA Repository ผ่านทาง Zenodo, ResearchGate หรือคลังของมหาวิทยาลัย
   - การติดต่อ Author Preprint จากนักวิจัยหลักโดยตรง
3. **ขั้นตอนเมื่อได้ไฟล์ PDF มาแล้ว**:
   - วางไฟล์ PDF ลงในโฟลเดอร์หมวดหมู่ที่เหมาะสมใน `research_library/`
   - รันคำสั่ง `python3 GeoThermAI/scripts/build_research_library_complete.py` เพื่อคำนวณ SHA-256 และอัปเดตสถานะจาก `MISSING_LOCAL_FILE` เป็น `SOURCE_VERIFIED`
