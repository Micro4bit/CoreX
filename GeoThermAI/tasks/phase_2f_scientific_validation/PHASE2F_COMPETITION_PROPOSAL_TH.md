# ข้อเสนอโครงการฉบับปรับปรุง (Phase 2F Scientific Validation) — GeoThermAI
**หมวด: Digital Energy Transition | นวัตกรรมปัญญาประดิษฐ์เพื่อการเปลี่ยนผ่านพลังงาน**
*สถานะ: ร่างข้อเสนอฉบับปรับปรุงความพร้อมเชิงวิทยาศาสตร์ (27 ตุลาคม 2569)*

---

## 1. ชื่อโครงการ (Project Title)

**GeoThermAI: ระบบปัญญาประดิษฐ์และสารสนเทศภูมิศาสตร์เชิงบูรณาการเพื่อคาดการณ์และจัดลำดับพื้นที่เป้าหมายการสำรวจพลังงานความร้อนใต้พิภพของประเทศไทย**  
*(GeoThermAI: An Integrated Geoscience AI and GIS Prospectivity Prediction System for Thailand Geothermal Exploration)*

---

## 2. หลักการและเหตุผล (Problem Statement & Rationale)

พลังงานความร้อนใต้พิภพ (Geothermal Energy) เป็นพลังงานสะอาดหมุนเวียนประเภท Baseload ที่มีเสถียรภาพสูงและปล่อยคาร์บอนต่ำ เหมาะสมอย่างยิ่งต่อยุทธศาสตร์ Decarbonization และการเปลี่ยนผ่านพลังงาน (Energy Transition) ของประเทศไทย อย่างไรก็ตาม **อุปสรรคสำคัญที่สุดของการพัฒนาพลังงานความร้อนใต้พิภพคือ "ความเสี่ยงและต้นทุนการเจาะสำรวจขั้นต้นที่สูงมาก (High Upstream Exploration Risk & Drilling Cost)"** ซึ่งเกิดจากการขาดแคลนแบบจำลองคาดการณ์ที่บูรณาการข้อมูลธรณีศาสตร์หลายมิติอย่างเป็นระบบ

ในอดีต การประเมินพื้นที่ศักยภาพในไทยมักพึ่งพาการสืบค้นข้อมูลเชิงคุณภาพหรืออาศัยเพียงระยะห่างจากน้ำพุร้อนผิวดิน ซึ่งไม่สามารถบ่งชี้ระบบกักเก็บใต้ผิวดินแบบปิด (Blind / Concealed Geothermal Systems) ได้ อีกทั้งการประยุกต์ใช้ AI ในอดีตมักประสบปัญหา **Spatial Data Leakage** (การรั่วไหลของข้อมูลระหว่างจุดฝึกและทดสอบ) และการทึกทักว่าจุดผิวดิน 47 จุดคือน้ำพุร้อน 47 แหล่งอิสระ ทั้งที่แท้จริงเป็นเพียงการผุดขึ้นผิวดินของโครงข่ายหักพังเดียวกัน (Hydrothermal Manifestations originating from common convective plumes)

**GeoThermAI** จึงได้รับการพัฒนาขึ้นภายใต้กรอบการวิจัยสากล **Replicate → Adapt → Validate → Improve** โดยนำระเบียบวิธี Geothermal Play Fairway Analysis (DeAngelo et al., 2024) และแบบจำลอง Positive-Unlabeled (PU) Machine Learning จาก USGS (Mordensky et al., 2023, 2025) มาปรับใช้กับบริบทธรณีวิทยาไทย เพื่อสร้างระบบคัดกรองและจัดลำดับความน่าจะเป็นของศักยภาพแหล่งกักเก็บ (Exploration Favorability Ranking) อย่างโปร่งใสและตรวจสอบหลักฐานย้อนหลังได้ทุกจุด

---

## 3. วัตถุประสงค์โครงการ (Project Objectives)

1. **พัฒนาระบบสารสนเทศภูมิศาสตร์ (GIS Platform) ตรวจสอบย้อนกลับได้ 100%:** บูรณาการชั้นข้อมูลธรณีวิทยา รอยเลื่อน โครงสร้าง 3 มิติ ระดับความสูงภูมิประเทศ (DEM) และข้อมูลการไหลของความร้อน (Heat Flow) พร้อมระบบบันทึกความไม่แน่นอนและสิทธิ์การเข้าถึงข้อมูล (Data Provenance & License Verification)
2. **พัฒนาระบบคัดกรองปัญญาประดิษฐ์แบบ Fail-Closed (ML Gate):** กำหนดเงื่อนไขตรวจสอบความพร้อม 9 ด้าน (วิทยาศาสตร์ ข้อมูล กฎหมาย สถิติ) โดยระบบจะปิดกั้นการทำนายเชิงตัวเลขโดยอัตโนมัติหากข้อมูลยังไม่ผ่านการรับรองจากผู้เชี่ยวชาญ เพื่อป้องกันการชี้นำการลงทุนที่ผิดพลาด
3. **สร้างระเบียบวิธีคัดกรองพื้นที่ด้วย Positive-Unlabeled (PU) Learning:** ปฏิบัติต่อพื้นที่ที่ยังไม่พบน้ำพุร้อนว่าเป็น "Unlabeled" ไม่ใช่ "Negative" เพื่อเปิดโอกาสในการค้นพบแหล่งกักเก็บใหม่ใต้ผิวดิน (Blind Geothermal Exploration)
4. **กำหนดมาตรฐาน Spatial Group-Preserving Cross-Validation:** ป้องกันการโอเวอร์ฟิตเชิงพื้นที่ด้วยการจัดกลุ่มน้ำพุร้อนที่อยู่ในระบบเดียวกันให้อยู่ใน Fold เดียวกัน และทดสอบความไวของระยะ Buffer สกัดกั้น (5–30 กม.) เพื่อรายงานความแม่นยำอย่างตรงไปตรงมา

---

## 4. ระเบียบวิธีวิจัยและแผนการดำเนินงาน (Methodology & Implementation Plan)

โครงการแบ่งการดำเนินงานออกเป็น 3 มิติที่ชัดเจน:

### มิติที่ 1: ส่วนงานที่สร้างเสร็จและใช้งานได้จริงในปัจจุบัน (Built & Verified GIS Foundation)
- **ระบบแผนที่และเวิร์กสเปซสำรวจหลักฐาน (Interactive Evidence Explorer):** รองรับการแสดงผลชั้นข้อมูลหิน รอยเลื่อน แหล่งน้ำพุร้อน จุดวัดความร้อน IHFC และโมเดลจำลองภูมิประเทศ 3 มิติ (3D Terrain Preview)
- **ระบบควบคุมสิทธิ์และความถูกต้องของพิกัด:** ตรวจสอบพิกัดจริง 47 จุด แยกพิกัดที่มีความสอดคล้อง (14 จุดภาคเหนือ), พิกัดที่ต้องระงับเนื่องจากคลาดเคลื่อน $>1$ กม. (2 จุด: `CR_02`, `CM_16`), และพิกัดชั่วคราวภาคใต้ (31 จุด)
- **ระบบ Sandbox จำลองวิธีวิจัย USGS (`geothermai.usgs_replication`):** สร้างสภาพแวดล้อมทดสอบแยกอิสระเพื่อ Replicate โมเดลของ Mordensky et al. (2023) จากข้อมูล Western USA เพื่อเปรียบเทียบมาตรฐานสากล โดยมีระบบ Guardrail ป้องกันการนำผลโมเดลต่างประเทศมาแอบอ้างเป็นศักยภาพของไทย

### มิติที่ 2: กรอบการวิจัยที่อยู่ระหว่างการควบคุมคุณภาพอย่างเข้มงวด (Gated Research Methodology)
- **การระงับโมเดลทำนายเชิงสถิติ (NO-GO Gate):** ล็อคระบบการฝึกสอนโมเดลไว้จนกว่าจะได้รับหนังสืออนุญาตข้อมูลอนุพันธ์จากกรมทรัพยากรธรณี (DMR) และการรับรองกลุ่มระบบน้ำพุร้อนจากนักอุทกธรณีวิทยา
- **การจัดหาข้อมูลภูมิประเทศเพิ่มเติม:** ตรวจพบว่าแบบจำลอง SRTM DEM ในพื้นที่ศึกษาภาคเหนือยังมีช่องว่าง 7 ระวาง (ครอบคลุม 41.7%) อยู่ระหว่างดาวน์โหลดจาก USGS EarthExplorer เพื่อให้ครอบคลุม 100%
- **การตรวจสอบความไวของ Buffer พื้นที่หลัง (Buffer Sensitivity Analysis):** ประเมินผลกระทบของการกันพื้นที่รอบจุดน้ำพุร้อนที่รัศมี 5, 10, 15, 20, และ 30 กม. ต่อการลดภาวะ Spatial Autocorrelation

### มิติที่ 3: ผลสัมฤทธิ์และผลกระทบในอนาคต (Expected Outcomes & Energy Impact)
- **Relative Favorability Map:** แผนที่แสดงระดับความน่าจะเป็นเชิงเปรียบเทียบของพื้นที่ศักยภาพสำหรับจัดลำดับความเร่งด่วนในการลงพื้นที่สำรวจจริง
- **ลดความเสี่ยงและงบประมาณการเจาะสำรวจ (De-risking Geothermal Wells):** ช่วยให้กรมพัฒนาพลังงานทดแทนฯ (พพ.), กฟผ. หรือภาคเอกชน สามารถคัดกรองและตัดพื้นที่ความเสี่ยงสูงออกไปก่อนตัดสินใจลงทุนขุดเจาะหลุมสำรวจมูลค่าหลายสิบล้านบาท

---

## 5. ความสอดคล้องกับเกณฑ์การแข่งขัน "Digital Energy Transition"

1. **Digital Innovation:** ผสานเทคโนโลยีภูมิสารสนเทศสมัยใหม่ (Cloud-native GIS, Vector Tiles, 3D Rendering) เข้ากับ Machine Learning Algorithms (Positive-Unlabeled Learning, Spatial Block CV)
2. **Energy Transition Enablement:** สนับสนุนการพัฒนาพลังงานสะอาดชนิดโหลดฐาน (Baseload Clean Energy) ซึ่งเป็นกุญแจสำคัญสู่เป้าหมาย Net Zero Greenhouse Gas Emissions ปี 2065 ของประเทศไทย
3. **Scientific Integrity & Governance:** แตกต่างจากข้อเสนอ AI ทั่วไปตรงที่มีระบบ ML Gate ป้องกันผลลวง (Hallucination/Leakage) และยึดมั่นในจรรยาบรรณข้อมูลอย่างเคร่งครัด

---

## 6. เอกสารอ้างอิงหลัก (Core References)

1. **Mordensky, T. P., et al. (2023).** When less is more: Machine learning geothermal prospectivity with limited data. *Geothermics*, 110, 102662. DOI: 10.1016/j.geothermics.2023.102662.
2. **Mordensky, T. P., et al. (2025).** Favorability mapping and uncertainty quantification of hydrothermal systems in the Great Basin. *Geothermics*, 125, 103450. DOI: 10.1016/j.geothermics.2025.103450.
3. **DeAngelo, J., et al. (2024).** Play Fairway Analysis Part 2: A GIS methodology for geothermal favorability mapping. *Geothermics*, 115, 102882. DOI: 10.1016/j.geothermics.2023.102882.
4. **Valavi, R., et al. (2019).** blockCV: An R package for generating spatially or environmentally separated folds for k-fold cross-validation in species distribution modelling. *Methods in Ecology and Evolution*, 10(2), 225-232. DOI: 10.1111/2041-210X.13107.
5. **Department of Mineral Resources (DMR). (2024).** Active Fault Zones and Northern Thailand 1:250,000 Geological Map Data. Open Data Portal, Thailand.
