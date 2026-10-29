# GeoThermAI — Source, Intellectual Property & License Notes

> **Research Data Stewardship Notice**:
> เอกสารและข้อมูลทั้งหมดใน `research_library/` ได้รับการจัดหมวดหมู่และตรวจสอบสิทธิ์ตามกฎหมายทรัพย์สินทางปัญญา เพื่อให้มั่นใจว่าการใช้งานภายในโครงการ CoreX / GeoThermAI มีความถูกต้องตามหลักนิติธรรม จริยธรรมการวิจัย และไม่ละเมิดลิขสิทธิ์ของบุคคลภายนอก

---

## 1. การจำแนกประเภทลิขสิทธิ์และสิทธิ์การเผยแพร่ (License Taxonomy)

โครงการ GeoThermAI กำหนดมาตรฐานการระบุสิทธิ์ 4 ระดับ:

1. **`RESTRICTED_LOCAL_ONLY` (สิทธิ์ศึกษาเฉพาะบุคคล / ภายในเครื่อง)**:
   - เอกสารวิชาการที่ติดลิขสิทธิ์จากสำนักพิมพ์พาณิชย์ (เช่น Elsevier, Wiley, Springer, GRC)
   - อนุญาตให้เก็บสำเนาไว้ในเครื่อง Local เพื่อการศึกษา ค้นคว้า และวิจัยแบบส่วนตัวตามข้อยกเว้น Fair Use / Research Exception
   - **ข้อห้ามเด็ดขาด**: ห้าม Commit ขึ้น Public Git Repository, ห้ามแจกจ่ายสำเนาต่อสาธารณะ, ห้ามเปิด API ให้ดาวน์โหลด PDF

2. **`RESTRICTED_GOVERNMENT_USE` (ข้อมูลหน่วยงานรัฐที่มีเงื่อนไข)**:
   - แผนที่, Shapefile รอยเลื่อน, และข้อมูลชั้นหินจากกรมทรัพยากรธรณี (DMR)
   - กฎหมายอนุญาตให้เข้าถึงเพื่อประโยชน์สาธารณะและงานวิชาการ แต่การนำข้อมูลต้นฉบับหรือ Derivative Products ไปเผยแพร่เชิงพาณิชย์ต้องได้รับหนังสืออนุญาตอย่างเป็นทางการ
   - โครงการได้จัดทำร่างหนังสือขออนุญาตไว้ใน `DMR_DATA_PERMISSION_REQUEST_TH.md`

3. **`PERMITTED_OPEN_ACCESS` / `PERMITTED_ATTRIBUTION_NONCOMMERCIAL`**:
   - บทความวิจัยและชุดข้อมูล Open Access ภายใต้สัญญาอนุญาต Creative Commons (CC BY 4.0 หรือ CC BY-NC-ND) เช่น Songklanakarin Journal of Science and Technology (Ngansom & Duerrast 2021) และ Mendeley Data (Kapong Geophysics)
   - สามารถอ้างอิง เผยแพร่ และใช้งานได้โดยต้องระบุที่มา (Attribution) อย่างชัดเจน

4. **`PUBLIC_DOMAIN`**:
   - ข้อมูลและรายงานของหน่วยงานรัฐบาลกลางสหรัฐฯ (USGS, NASA) เช่น USGS Data Release P9V1Q9XM และข้อมูลระดับความสูง SRTM 30m
   - เป็นผลงานที่ไม่มีลิขสิทธิ์ตามกฎหมายสหรัฐฯ (U.S. Government Work)

5. **`REPO_INTERNAL` / `PROJECT_PROPRIETARY` (MIT License)**:
   - ซอร์สโค้ด, สคริปต์, รายงานการทดสอบ (Implementation Reports), Gate Reports, และเอกสารสถาปัตยกรรมที่พัฒนาขึ้นโดยทีมงาน GeoThermAI (CoreX)

---

## 2. รายละเอียดสิทธิ์แยกตามแหล่งข้อมูลหลัก

### A. กรมทรัพยากรธรณี (Department of Mineral Resources - DMR), กระทรวงทรัพยากรธรรมชาติและสิ่งแวดล้อม
- **ชุดข้อมูล**:
  - แผนที่น้ำพุร้อนประเทศไทย มาตราส่วน 1:1,000,000 (`dmr_thailand_hot_springs_map.pdf`)
  - Shapefile แนวรอยเลื่อนมีพลังภาคเหนือ 630 แนว (`N_ZONE_ACTIVEFAULT_20230419_091427.shp`)
  - ข้อมูลหมวดหินธรณีวิทยา 1:250,000 ภาคเหนือ 1,266 แปลง (`dmr-rock-units-north.full.geojson`)
- **การปฏิบัติตามกฎหมาย**:
  - ข้อมูลถูกเก็บไว้ในพื้นที่ Local ของระบบ
  - ชั้นข้อมูล GIS ขนาดใหญ่ถูกคัดแยกไว้ใน `DATASET_POINTERS.csv` และถูกเพิกถอนจากการส่งขึ้น Public Git ผ่าน `.gitignore`
  - มีการจัดทำเอกสาร `DMR_DATA_PERMISSION_REQUEST_TH.md` เพื่อขอความอนุเคราะห์ใช้ข้อมูลในการวิจัยและพัฒนาแบบจำลองเชิงอนุพันธ์ (Derivative Works) อย่างถูกต้อง

### B. คณะกรรมาธิการความร้อนใต้พิภพสากล (International Heat Flow Commission - IHFC)
- **ชุดข้อมูล**: Global Heat Flow Database 2024 (`ihfc_thailand_qc.csv`)
- **สิทธิ์การใช้งาน**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **การอ้างอิงที่ถูกต้อง**: *International Heat Flow Commission (2024). Global Heat Flow Database. DOI: 10.5880/IHFC.2024.001*

### C. องค์การนาซา และ สำรวจธรณีวิทยาสหรัฐฯ (NASA / USGS)
- **ชุดข้อมูล**:
  - Shuttle Radar Topography Mission (SRTM) 1-ArcSecond 30m Global DEM (`N17E099.tif`, `N18E099.tif`, `N19E098.tif`, `N19E099.tif`, `N20E099.tif`)
  - USGS Data Release for Mordensky 2023 (DOI: 10.5066/P9V1Q9XM)
- **สิทธิ์การใช้งาน**: Public Domain (ไม่มีข้อจำกัดด้านลิขสิทธิ์)

### D. วารสารวิชาการและการจัดพิมพ์ (Academic Publishers)
- **GRC Transactions** (Wood & Singharajwarapan 2014): สิทธิ์ทางวิชาการของ Geothermal Resources Council เก็บเพื่อการวิจัยภายใน
- **SJST / Prince of Songkla University** (Ngansom & Duerrast 2021): Open Access เผยแพร่ได้โดยไม่แสวงหากำไร
- **Mendeley Data** (Kapong Geophysics 2021): CC BY 4.0

### E. หน่วยงานนโยบายภาครัฐ (EPPO, BOI, กระทรวงพลังงาน)
- **เอกสาร**: ข้อมูลร่าง PDP2026, นโยบายส่งเสริมการลงทุน Data Center และ AI
- **สิทธิ์การใช้งาน**: เอกสารราชการเพื่อการรับฟังความคิดเห็นสาธารณะและการส่งเสริมการลงทุน สามารถนำมาสังเคราะห์ในเชิงนโยบายได้โดยระบุแหล่งที่มา

---

## 3. นโยบายการจัดการ Git และความปลอดภัยข้อมูล (Git Security Policy)
1. **ห้าม Commit Binary PDF ที่มีลิขสิทธิ์**: ไฟล์ PDF วิจัยทั้งหมดใน `research_library/` ได้รับการยกเว้นผ่าน `.gitignore`
2. **อนุญาตเฉพาะ Metadata และ Index**: ไฟล์ Markdown, CSV Index, และ BibTeX เท่านั้นที่จัดเก็บบน Version Control เพื่อเป็น Living Research Catalog
3. **เกตปิดอัตโนมัติ (Fail-Closed Gate)**: ระบบโมเดล Machine Learning จะไม่ถูกสั่งรันหากยังไม่มีเอกสารยืนยันสิทธิ์จาก DMR เป็นลายลักษณ์อักษร
