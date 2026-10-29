# GeoThermAI Phase 2F — Dataset Licensing & Legal Reuse Matrix
**Intellectual Property, Redistribution Terms, and Regulatory Clearance Framework**

**Document Version:** 1.0 (Phase 2F)  
**Date:** 2026-10-27 (Asia/Bangkok)  
**Status:** AUDITED — **FORMAL DMR CLEARANCE PENDING (NO FICTIONAL APPROVALS)**

---

## 1. Master Dataset License & Usage Clearance Matrix

| Dataset Identifier | Publishing Authority | Native License / Stated Terms | Descriptive GIS Display | Machine Learning Training | Derivative Map Release | Commercial Exploration Advisory | Required Attribution & Notes |
|---|---|---|:---:|:---:|:---:|:---:|---|
| **DMR 1:250k Northern Geology** | Department of Mineral Resources (DMR), Thailand | Government agency database (data.dmr.go.th / ArcGIS REST); Terms unverified for external derivative redistribution | ✅ **PERMITTED** (Contextual visual overlay) | ⚠️ **CONDITIONAL** (Requires written clarification on ML ingestion) | ❌ **BLOCKED** (Derivative prospectivity map release unconfirmed) | ❌ **BLOCKED** (Commercial redistribution prohibited without formal clearance) | "Geological data provided by Department of Mineral Resources, Thailand (2023)." Must retain original legend symbols. |
| **DMR Active Fault Zones** | Department of Mineral Resources (DMR), Thailand | Contradictory: Catalog lists Open Government / CC-BY, but inner metadata states non-commercial and prohibits legal citation | ❌ **BLOCKED** (Disabled in UI) | ❌ **STRICTLY BLOCKED** (Prohibited in training pipeline) | ❌ **BLOCKED** (Cannot publish fault proximity derivatives) | ❌ **BLOCKED** | Conflicting catalog terms must be resolved in writing by DMR prior to any usage. |
| **SRTM Global 1 Arc-Second DEM** | NASA / U.S. Geological Survey (USGS) | Public Domain (U.S. Government work) | ✅ **PERMITTED** | ✅ **PERMITTED** (Terrain feature engineering) | ✅ **PERMITTED** | ✅ **PERMITTED** | "SRTM data courtesy of NASA and USGS." Attribution requested. 5 tiles verified in repository. |
| **IHFC Global Heat Flow 2024** | International Heat Flow Commission / GFZ Potsdam | Creative Commons Attribution 4.0 International (CC BY 4.0) | ✅ **PERMITTED** (Descriptive point observation only) | ❌ **BLOCKED FOR INTERPOLATION** (Methodological barrier, not license) | ⚠️ **CONDITIONAL** (Point display only; no interpolated surface) | ✅ **PERMITTED** (Under CC-BY 4.0 attribution) | "Fuchs, S., et al. (2024). The Global Heat Flow Database: 2024 Release. GFZ Data Services. DOI:10.5880/fidgeo.2024.014." |
| **Northern Geothermal Registry** | Chiang Mai University / DMR (Wood & Singharajwarapan, 2014) | Academic scientific publication (Academic Fair Use / Attribution) | ✅ **PERMITTED** | ⚠️ **CONDITIONAL** (Requires expert system grouping; withheld CR_02/CM_16) | ⚠️ **CONDITIONAL** | ⚠️ **CONDITIONAL** | "Wood, S. H., & Singharajwarapan, S. (2014). Geothermal energy resources of northern Thailand." |
| **Southern Geothermal Registry** | Prince of Songkla University (Ngansom & Duerrast, 2021) | Academic scientific publication (Academic Fair Use / Attribution) | ⚠️ **PROVISIONAL** (Excluded from northern pilot) | ❌ **EXCLUDED** (Provisional coordinates) | ❌ **BLOCKED** | ❌ **BLOCKED** | "Ngansom, W., & Duerrast, H. (2021). Songklanakarin J. Sci. Technol." Requires UTM Zone 47N/48N resolution. |
| **Landsat C2 L2 Surface Temp** | USGS / NASA Landsat Program | Public Domain (USGS Open Data Policy) | ❌ **NOT LOADED** (0 usable rasters acquired) | ❌ **DISABLED** (Zero valid rasters) | ❌ **DISABLED** | ❌ **DISABLED** | USGS Landsat data policy is free and open, but zero valid GeoTIFFs were acquired in Phase 2D/2E. |
| **Natural Earth Admin-0** | Natural Earth Consortium | Public Domain (Free for all purposes) | ✅ **PERMITTED** | ✅ **PERMITTED** (Spatial clipping mask) | ✅ **PERMITTED** | ✅ **PERMITTED** | Boundary mask verified in repository (`ne_10m_admin_0_countries.zip`). |
| **GGMplus Satellite Gravity** | Curtin University / Western Australian Geodesy Group | Open Access Research Dataset (Creative Commons / Academic Citation) | ❌ **NOT ACQUIRED** | ❌ **NOT ACQUIRED** | ❌ **NOT ACQUIRED** | ❌ **NOT ACQUIRED** | "Hirt, C., et al. (2013). GGMplus." Research lead for future acquisition. |

---

## 2. Official DMR Clarification & Inquiry Packet (Ready to Transmit)

Below is the official Thai language correspondence packet prepared for submission to the Department of Mineral Resources (DMR).

```markdown
เรื่อง: ขอความอนุเคราะห์ชี้แจงสิทธิ์การใช้และเผยแพร่ผลงานอนุพันธ์ของข้อมูลภูมิสารสนเทศทางธรณีวิทยา
เรียน: ผู้อำนวยการกองเทคโนโลยีสารสนเทศมรดกทางธรณีและข้อมูลภูมิสารสนเทศ กรมทรัพยากรธรณี

ตามที่คณะผู้พัฒนาโครงการวิจัย GeoThermAI (CoreX) ภายใต้การสนับสนุนงานวิจัยด้านพลังงานสะอาด ได้ดำเนินการพัฒนา
ระบบปัญญาประดิษฐ์และสารสนเทศภูมิศาสตร์สนับสนุนการตัดสินใจในการคัดกรองพื้นที่เป้าหมายการสำรวจพลังงานความร้อนใต้พิภพ
(Geothermal Exploration Favorability Decision Support System) เพื่อส่งเสริมการเปลี่ยนผ่านสู่พลังงานหมุนเวียนของประเทศไทย

ในการนี้ คณะผู้วิจัยได้ศึกษาข้อมูลภูมิสารสนเทศที่เผยแพร่ผ่านระบบสืบค้นข้อมูลของกรมทรัพยากรธรณี (data.dmr.go.th และ ArcGIS REST)
และมีความประสงค์ที่จะนำข้อมูลดังกล่าวมาใช้เป็นตัวแปรสนับสนุนทางวิชาการ โดยยึดมั่นในจรรยาบรรณวิจัยและไม่ละเมิดสิทธิ์ในทรัพย์สินทางปัญญา

จึงใคร่ขอความอนุเคราะห์จากกรมทรัพยากรธรณี โปรดพิจารณาชี้แจงเป็นลายลักษณ์อักษรในประเด็นสิทธิ์การใช้งานดังต่อไปนี้:

1. สิทธิ์การเข้าถึงและประมวลผลข้อมูล (Data Access & Processing):
   - สิทธิ์ในการดาวน์โหลดและจัดเก็บข้อมูลเรขาคณิต (Geometry) และตารางคุณลักษณะ (Attributes) ของ:
     (ก) ข้อมูลกลุ่มรอยเลื่อนมีพลัง (Active Fault Zones)
     (ข) แผนที่ธรณีวิทยาประเทศไทย มาตราส่วน 1:250,000 (Geological Units 1:250,000)
2. สิทธิ์ในการนำเข้าสู่กระบวนการเรียนรู้ของเครื่อง (Machine Learning Training):
   - สิทธิ์ในการนำชั้นข้อมูลดังกล่าวไปใช้เป็นตัวแปรทำนาย (Predictor Features) ร่วมกับอัลกอริทึมปัญญาประดิษฐ์เพื่อการวิจัยทางวิชาการ
3. สิทธิ์การสร้างและเผยแพร่ข้อมูลอนุพันธ์ (Derivative Works):
   - สิทธิ์ในการคำนวณและเผยแพร่ข้อมูลอนุพันธ์เชิงพื้นที่ เช่น แผนที่ระยะห่างจากรอยเลื่อน (Fault Proximity Surface) 
     และแผนที่จัดลำดับความเหมาะสมของพื้นที่ (Prospectivity Favorability Map) ต่อสาธารณะในรายงานวิจัยและการประชุมวิชาการ
4. สิทธิ์การแสดงผลผ่านระบบสารสนเทศ (Web GIS Display):
   - ข้อกำหนดในการนำชั้นข้อมูลมาแสดงผลในรูปแบบแผนที่เชิงบรรยาย (Contextual Overlay) ผ่านระบบ Web Application
5. สิทธิ์และการต่อยอดเชิงพาณิชย์ (Commercial Advisory Use):
   - ข้อจำกัดทางกฎหมายหากในอนาคตผลการวิจัยได้รับการต่อยอดเพื่อให้บริการวิเคราะห์ความเสี่ยงเชิงพื้นที่แก่ภาคเอกชนผู้พัฒนาโรงไฟฟ้า
6. รูปแบบการอ้างอิงแหล่งที่มาที่ถูกต้อง (Attribution Standards):
   - ข้อความการให้เกียรติและอ้างอิงกรมทรัพยากรธรณีที่ทางกรมฯ กำหนดให้ระบุในผลงานตีพิมพ์และบนหน้าเว็บแอปพลิเคชัน

ทั้งนี้ คณะผู้วิจัยขอเรียนยืนยันว่า ในระหว่างที่ยังไม่ได้รับหนังสือชี้แจงหรือการอนุมัติเป็นลายลักษณ์อักษรจากกรมทรัพยากรธรณี 
ทางโครงการได้ "ปิดกั้นการนำเข้าข้อมูลรอยเลื่อนสู่การฝึกโมเดล AI" (Blocked from ML Training) และ "ระงับการส่งออกข้อมูลเรขาคณิตดิบ" 
อย่างเคร่งครัดตามมาตรฐาน Data Governance

ขอแสดงความนับถืออย่างยิ่ง

(ลงนาม)........................................................
(คณะผู้พัฒนาโครงการวิจัย GeoThermAI)
```

---

## 3. Legal and Regulatory Enforcement Policy

1. **Fail-Closed Gate Binding:** Condition `predictors_licensed_and_covered` and `output_release_approved` in `geothermai.ml_gate` remain strictly set to `approved: false` until an official signed response from DMR is received and logged in `tasks/phase_2f_scientific_validation/evidence/`.
2. **Web UI Export Restrictions Maintained:** The public web application retains existing UI controls disabling vector export of DMR layers, accompanied by explanatory tooltips informing researchers of pending administrative review.
