# GeoThermAI — Master Literature Map and Scientific Synthesis

> **Research Integrity & Traceability Matrix**:
> เอกสารนี้ทำหน้าที่เป็น **Literature Map** เชื่อมโยงหลักฐานทางวิทยาศาสตร์ นโยบายพลังงาน และระเบียบวิธีวิจัยทั้งหมดเข้ากับไปป์ไลน์การทำงานจริงของ GeoThermAI (CoreX)
> โดยจำแนกอย่างเคร่งครัดระหว่าง:
> 1. สิ่งที่งานวิจัยดั้งเดิมทำไว้แล้ว (Prior Art)
> 2. สิ่งที่ GeoThermAI นำมาดัดแปลง (Adapted Innovation)
> 3. สิ่งที่ยังเป็นสมมติฐานที่ต้องรอการทดสอบด้วยข้อมูลจริง (Hypotheses Under Gate)

---

## 1. การรองรับ Pain Point ระดับ PDP2026 / Data Center / ความมั่นคงพลังงาน / เศรษฐกิจ

### A. ปัญหาเชิงโครงสร้างของระบบพลังงานไทย
- **เป้าหมาย PDP2026 (EPPO 2026)**: แผนพัฒนากำลังผลิตไฟฟ้าของประเทศไทยกำหนดสัดส่วนพลังงานหมุนเวียนไว้สูงถึง 51% ภายในปี 2037 เพื่อมุ่งสู่ Carbon Neutrality
- **ความท้าทายจาก Hyperscale AI Data Center (BOI 2026)**: การอนุมัติการลงทุนศูนย์ข้อมูลและคลาวด์ขนาดใหญ่ในไทย (AWS, Google, Microsoft, GDS, OneAsia) มูลค่ารวมกว่า 1.6 แสนล้านบาท ก่อให้เกิดความต้องการไฟฟ้าแบบ **24/7 Firm Clean Power** (ไฟฟ้าสะอาดที่จ่ายได้อย่างต่อเนื่องสม่ำเสมอตลอด 24 ชั่วโมง ความน่าเชื่อถือ 99.999%)
- **ข้อจำกัดของพลังงานหมุนเวียนแบบผันผวน (Intermittent Renewables)**: แสงอาทิตย์ (Solar) จ่ายไฟได้เฉพาะกลางวัน (Capacity Factor 15–20%) และลม (Wind) มีความผันแปรสูง หากไม่มีระบบกักเก็บพลังงาน (BESS) ขนาดมหึมาซึ่งมีต้นทุนสูงมาก จะไม่สามารถรองรับโหลดศูนย์ข้อมูล AI ได้

### B. หลักฐานที่รองรับบทบาทของพลังงานความร้อนใต้พิภพ
- **รายงาน IEA (2024) *The Future of Geothermal Energy***: ยืนยันว่า Geothermal เป็นหนึ่งในแหล่งพลังงานหมุนเวียนไม่กี่ชนิดที่ให้ **Capacity Factor สูงกว่า 90–95%** ใช้พื้นที่หน้าดินน้อยที่สุดต่อเมกะวัตต์ (Footprint ต่ำกว่า Solar 80–90%) และมีความเสถียรต่อสภาพอากาศ
- **เอกสารโครงการ `PHASE2G_PDP2026_DATACENTER_EVIDENCE_TH.md`**: สังเคราะห์ตัวเลขเศรษฐศาสตร์พบว่า ต้นทุน LCOE ของโรงไฟฟ้าความร้อนใต้พิภพแบบไบนารี (Binary Cycle) อยู่ที่ประมาณ 0.06 – 0.09 USD/kWh ซึ่งสามารถแข่งขันได้กับการรวม Solar + 4-hour Battery (> 0.12 USD/kWh) และตอบโจทย์เกณฑ์ Direct PPA ของ BOI ได้อย่างสมบูรณ์แบบ

---

## 2. การรองรับ Geothermal Resource Uncertainty และ Exploration Risk

### A. ความเสี่ยงจากการเจาะหลุมสำรวจ (Drilling Risk)
- ในการสำรวจธรณีความร้อนระยะแรก การเจาะหลุมสำรวจ (Exploration Well) มีค่าใช้จ่ายสูงมาก (2–6 ล้านดอลลาร์สหรัฐต่อหลุม) และมีอัตราความสำเร็จในพื้นที่ Greenfield ทั่วโลกเพียง 20–30% หากอาศัยเพียงการตรวจผิวดิน
- **DeAngelo et al. (2024)** และ **Williams & DeAngelo (2008)**: นำเสนอระเบียบวิธี **Play Fairway Analysis (PFA)** เพื่อลดความเสี่ยง โดยการประเมินแยกเป็น 3 องค์ประกอบหลัก:
  1. **Heat Engine**: แหล่งกำเนิดความร้อน (หินแกรนิตกัมมันตรังสี, แนวเทือกเขาหินแกรนิต Triassic ในไทย, อัตราการไหลของความร้อน)
  2. **Permeability**: ความสามารถในการซึมผ่านของหิน (ความหนาแน่นของรอยเลื่อนมีพลัง, ความเค้นเปลือกโลก, รอยต่อรอยเลื่อน)
  3. **Fluid & Seal**: แหล่งกักเก็บของไหลและชั้นหินปิดกั้น (ระบบน้ำบาดาล, ธรณีเคมี)

### B. การวัดและจำกัดความไม่แน่นอนใน GeoThermAI
- **Mordensky et al. (2025)**: นำเสนอการประเมินความไม่แน่นอนด้วย **Monte Carlo Simulation** และการจัดชั้นความเชื่อมั่นของข้อมูลแบบ Ordinal
- โครงการ GeoThermAI นำแนวทางนี้มาสร้าง **Uncertainty Overlay Layer** ในระบบตัดสินใจ (`PHASE2G_DECISION_SUPPORT_UX_SPEC.md`) โดยไม่แสดงเฉพาะค่าความน่าจะเป็นแบบจุดเดียว (Point Estimate) แต่แสดงคู่กับดัชนีความไม่แน่นอนเชิงพื้นที่ (Spatial Confidence Metric)

---

## 3. การรองรับ Geothermal Favorability Modeling / PFA / Logistic Regression / XGBoost

### A. ระเบียบวิธีวิจัยหลักจากวรรณกรรมสากล
- **Mordensky et al. (2023) *When less is more***:
  - ใช้ **Logistic Regression (LR)** เป็นโมเดลพื้นฐานเชิงเส้นที่สามารถตีความได้ (interpretable linear baseline) และใช้ **Extreme Gradient Boosting (XGBoost)** เพื่อจับความสัมพันธ์แบบไม่เป็นเส้นตรง (non-linear interactions)
  - ค้นพบข้อสรุปสำคัญ: **"การใส่ตัวแปรมากเกินไปทำให้โมเดล Overfit และมี False Positive สูง"** การตัดทอนตัวแปร (Feature Pruning) เหลือเฉพาะตัวแปรที่มีความหมายทางฟิสิกส์ธรณีจริง ช่วยให้โมเดลมี Generalization สูงขึ้น

### B. การจำลองซ้ำบนข้อมูลมาตรฐาน USGS (Replication Sandbox)
- โครงการ GeoThermAI ได้สร้างสภาพแวดล้อมทดสอบการจำลองซ้ำแยกต่างหาก (`GeoThermAI/src/geothermai/usgs_replication.py`) โดยใช้ข้อมูลจริงจาก **USGS 2023 Data Release (DOI: 10.5066/P9V1Q9XM)**
- **ผลการทดสอบที่ผ่านการตรวจสอบจริง (`PHASE2F2_REPLICATION_RESULTS.md`)**:
  - Logistic Regression Replication AUC: **0.812**
  - XGBoost Replication AUC: **0.835**
- **ข้อกำหนดทางจริยธรรม**: โครงการระบุชัดเจนว่าคะแนน AUC 0.835 นี้เป็น **คะแนนจำลองบนข้อมูล Great Basin สหรัฐอเมริกาเท่านั้น ห้ามนำมาอ้างว่าเป็นความแม่นยำของโมเดลพื้นที่ประเทศไทย**

---

## 4. การรองรับ Data Harmonization, Ground Truth, PU Learning และ Spatial Validation

### A. การจัดการจุดบ่งชี้ความร้อน (Ground Truth Manifestations)
- **Wood & Singharajwarapan (2014)**: ให้ข้อมูล 16 แหล่งน้ำพุร้อนภาคเหนือ พร้อมพิกัด UTM/DMS และอุณหภูมิผิวดิน
- **Ngansom & Duerrast (2021)**: ให้ข้อมูล 31 จุดน้ำพุร้อนใน 9 จังหวัดภาคใต้
- **การตรวจสอบความถูกต้องเชิงพิกัดของ GeoThermAI (`coordinate_qc_report.md`, `PHASE2G_GROUND_TRUTH_ADJUDICATION.csv`)**:
  - ตรวจพบว่าพิกัด `CR_02` (โป่งป่าเส้า) มีระยะคลาดเคลื่อนระหว่าง UTM และ DMS ถึง **1,872.76 เมตร** จึงต้องสั่ง Withhold ห้ามนำมาเทรน
  - จุด `CM_16` ไม่มีค่า DMS ให้ตรวจสอบ จึงสั่ง Withhold
  - จุดภาคใต้ทั้ง 31 จุด ไม่มีระบุ UTM Zone ชัดเจนในตาราง จึงต้องคงสถานะ **Provisional (รอการยืนยันโซน)**
  - ยืนยันว่า **47 แถวข้อมูลไม่ได้เท่ากับ 47 ระบบธรณีความร้อนอิสระ** (หลายจุดอยู่ในแอ่งเดียวกัน เช่น สันกำแพง และ ฝาง) จึงต้องจัดกลุ่ม (Spatial Clustering) เพื่อป้องกัน Data Leakage

### B. Positive-Unlabeled (PU) Learning และการแก้ Selection Bias
- **Bekker & Davis (2020)**: ชี้ให้เห็นว่าในงานสำรวจแร่ธาตุและพลังงาน พื้นที่ที่ไม่มีบ่อน้ำพุร้อนร้อนไม่ใช่ "บ่อแห้ง (True Negative)" แต่เป็นพื้นที่ที่ยังไม่ได้สำรวจ (Unlabeled)
- การสุ่มพื้นหลังแบบ Naive Random Negative จะทำให้โมเดลเกิด Bias รุนแรง GeoThermAI จึงใช้ระเบียบวิธี **Positive-Unlabeled Learning** พร้อมตรวจสอบสมมติฐาน SCAR (Selected Completely At Random) ตามที่บันทึกไว้ใน `PHASE2F1_PU_LEARNING_AUDIT.md`

### C. Spatial Cross-Validation และ Spatial Blocking
- **Roberts et al. (2017)** และ **Valavi et al. (2019) *blockCV***:
  - พิสูจน์ว่าการสุ่ม Cross-Validation แบบธรรมดา (Random K-Fold) บนข้อมูลเชิงพื้นที่จะทำให้โมเดลจำพิกัดและค่าความผิดปกติของเซลล์ข้างเคียง ทำให้ผลประเมินสูงเกินจริง (Overoptimistic) กว่า 25–40%
  - GeoThermAI กำหนดให้ใช้ **Spatial Block Cross-Validation** โดยกันข้อมูลทั้งระบบ (Cluster) ออกจากการเทรน และทำการทดสอบความไวของระยะ Buffer (10 km, 20 km, 30 km) ตามเอกสาร `PHASE2F_SPATIAL_VALIDATION_TH.md`

---

## 5. การรองรับ Environmental Screening และผลกระทบเศรษฐกิจ สังคม สิ่งแวดล้อม

### A. กรอบการคัดกรองพื้นที่อนุรักษ์ (Environmental Exclusion Framework)
- เอกสาร `PHASE2G_ENVIRONMENTAL_SCREENING_RULES.md` กำหนดเกณฑ์คัดกรองพื้นที่ต้องห้ามเด็ดขาด (Fatal-Flaw Criteria) ตามกฎหมายไทย:
  - **พื้นที่ห้ามเข้าทำประโยชน์**: อุทยานแห่งชาติ (National Parks), เขตรักษาพันธุ์สัตว์ป่า (Wildlife Sanctuaries), และพื้นที่ลุ่มน้ำชั้น 1A (Class 1A Watershed) ตามมติ ครม.
  - **แนวกันชน (Buffer Zone)**: กำหนดระยะกันชน 1 กิโลเมตรจากแนวเขตพื้นที่คุ้มครอง
  - ช่วยให้นักลงทุนและผู้กำหนดนโยบายทราบได้ทันทีว่าพื้นที่ที่มีศักยภาพความร้อนสูงจุดใดติดข้อจำกัดทางกฎหมายสิ่งแวดล้อม

### B. ตัวชี้วัดผลกระทบและการมีส่วนร่วมของชุมชน (Impact KPIs)
- เอกสาร `PHASE2G_IMPACT_KPI_PROTOCOL_TH.md` กำหนดกรอบการประเมิน:
  - ปริมาณการลดก๊าซเรือนกระจก (tCO2e Abated) เมื่อเทียบกับโรงไฟฟ้าก๊าซธรรมชาติหรือดีเซล
  - การใช้ประโยชน์พลังงานความร้อนโดยตรงแบบลดหลั่น (Direct-Use & Cascade Utilization) เช่น การอบแห้งผลิตผลทางการเกษตร ห้องเย็นอุณหภูมิต่ำ และการท่องเที่ยวเชิงบำบัดสุขภาพ
  - กองทุนพัฒนาชุมชนรอบโรงไฟฟ้าและการจ้างงานในท้องถิ่น

---

## 6. สรุปความก้าวหน้า: สิ่งที่ทำแล้ว / ดัดแปลง / สมมติฐานที่รอทดสอบ

| ด้านการวิจัย | งานเดิมในอดีต (Prior Art) | สิ่งที่ GeoThermAI นำมา Adapt | สิ่งที่เป็นสมมติฐานที่รอทดสอบ (Hypotheses) |
|---|---|---|---|
| **การทำนายความน่าจะเป็น (Favorability ML)** | ใช้ Random Negative สุ่มทั่วประเทศ เกิด False Positive สูง | ใช้ PU Learning + Pruning ตัดตัวแปรระยะห่างน้ำพุร้อนออก | โมเดลแบบผสม LR+XGBoost จะให้เสถียรภาพสูงสุดในธรณีวิทยาไทย |
| **การทดสอบความถูกต้อง (Validation)** | Random K-Fold ธรรมดา ซึ่งเกิด Spatial Data Leakage | Spatial Block Fold + Co-withholding ตามระบบน้ำพุร้อน | การใช้ Buffer 20 กม. เพียงพอที่จะตัดการรั่วไหลของ Spatial Autocorrelation |
| **ความพร้อมของข้อมูล (Data Readiness)** | สันนิษฐานว่ามีข้อมูลครบ ทั้งรอยเลื่อน ความร้อน และ Landsat | ทำ Audit จริง: พบว่า Landsat เมฆหนาเกินไป และความร้อนมีเฉพาะในแอ่ง | การใช้ Structural Permeability Proxy ทดแทน LST จะให้สัญญาณที่แม่นยำกว่า |
| **ธรรมาภิบาลข้อมูล (Governance & IP)** | นำ Shapefile และแผนที่มาใช้โดยไม่ตรวจสอบสิทธิ์ | ทำ License Matrix และทำหนังสือขออนุญาตใช้ข้อมูลอย่างเป็นทางการจาก DMR | DMR จะอนุมัติให้ใช้ชั้นข้อมูลรอยเลื่อนและธรณีวิทยาในการวิจัยแบบจำลอง |
| **การนำไปใช้จริง (Decision Support)** | มีเฉพาะแผนที่ Heatmap ทางธรณีวิทยา | รวมเกณฑ์สิ่งแวดล้อม, สายส่งไฟฟ้า, และความต้องการ Data Center เข้าใน UI | โรงไฟฟ้าความร้อนใต้พิภพขนาดเล็ก (1-5 MW) สามารถตอบสนองโหลด Data Center ในพื้นที่ได้จริง |
