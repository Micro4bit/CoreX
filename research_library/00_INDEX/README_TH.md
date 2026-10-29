# GeoThermAI — คู่มือการใช้งานคลังงานวิจัยและเอกสารอ้างอิง (Research Library)

ยินดีต้อนรับสู่ **GeoThermAI Research Library** ซึ่งเป็นศูนย์รวมเอกสารงานวิจัย เอกสารนโยบายพลังงาน ข้อมูลธรณีฟิสิกส์ และหลักฐานทางวิทยาศาสตร์ทั้งหมดของโครงการ GeoThermAI (CoreX)

คลังเอกสารนี้ถูกออกแบบตามมาตรฐาน **Research Data Stewardship & Scientific Integrity** เพื่อให้สามารถสืบค้น ตรวจสอบย้อนกลับ (Traceability) และอ้างอิงได้อย่างโปร่งใส

---

## 1. โครงสร้างโฟลเดอร์ของคลังเอกสาร

```text
research_library/
├── 00_INDEX/                                   # ศูนย์ดัชนี รายงานการตรวจสอบ และคู่มือ
│   ├── README_TH.md                            # คู่มือการใช้งานคลังเอกสาร (เอกสารนี้)
│   ├── RESEARCH_MASTER_INDEX.csv               # ดัชนีหลัก 20 คอลัมน์ของเอกสารทั้งหมด
│   ├── RESEARCH_MASTER_INDEX.md                # Literature Map วิเคราะห์ความเชื่อมโยงกับโครงการ
│   ├── DUPLICATES_AND_VERSIONS.csv             # รายงานการตรวจสอบไฟล์ซ้ำและการชนกันของเวอร์ชัน
│   ├── MISSING_REFERENCES.md                   # รายการเอกสารเป้าหมายที่ยังไม่มี PDF ในเครื่อง Local
│   ├── DATASET_POINTERS.csv                    # บันทึกพอยน์เตอร์ไปยังชุดข้อมูล GIS/Raster ขนาดใหญ่
│   ├── SOURCE_AND_LICENSE_NOTES.md             # สรุปสถานะลิขสิทธิ์และข้อกำหนดการใช้งาน
│   └── COLLECTION_EXECUTION_LOG.md             # บันทึกการทำงานและผลการตรวจสอบความสมบูรณ์
├── 01_GEOTHERMAL_FAVORABILITY_AND_PFA/          # งานวิจัยศักยภาพความร้อนใต้พิภพและ Play Fairway Analysis
├── 02_AI_ML_AND_STATISTICAL_METHODS/            # ระเบียบวิธีปัญญาประดิษฐ์ Machine Learning และสถิติ
├── 03_SPATIAL_CV_PU_AND_UNCERTAINTY/           # Spatial Cross-Validation, PU Learning, และการประเมินความไม่แน่นอน
├── 04_THAILAND_GEOSCIENCE_AND_GEOPHYSICS/      # ธรณีวิทยา ธรณีฟิสิกส์ และบ่อน้ำพุร้อนในประเทศไทย (PDF หลัก)
├── 05_HYDROGEOLOGY_GEOCHEMISTRY_AND_HEAT_FLOW/  # อุทกธรณีวิทยา ธรณีเคมี และการกระจายตัวของ Heat Flow
├── 06_SATELLITE_REMOTE_SENSING_AND_GIS/        # รีโมตเซนซิงดาวเทียม (Landsat, SRTM) และการวิเคราะห์ GIS
├── 07_ENERGY_POLICY_PDP2026_AND_DATACENTER/    # นโยบายพลังงาน PDP2026, กฎระเบียบ BOI, และข้อมูล Data Center
├── 08_ENVIRONMENT_ECONOMICS_AND_SOCIAL_IMPACT/ # การคัดกรองพื้นที่อนุรักษ์ เศรษฐศาสตร์พลังงาน (LCOE) และผลกระทบ
├── 09_PROJECT_RESEARCH_REPORTS_AND_PROTOCOLS/  # รายงานการวิจัยภายในโครงการ ข้อเสนอโครงการ และเกตการทดสอบ
└── 10_SUPPLEMENTARY_AND_CITATIONS/             # ข้อมูลประกอบ ไฟล์บรรณานุกรม BibTeX และรายการตรวจสอบ
```

---

## 2. วิธีการสืบค้นเอกสาร

1. **ค้นหาผ่านดัชนี CSV (`RESEARCH_MASTER_INDEX.csv`)**:
   - เปิดไฟล์ด้วยโปรแกรม Spreadsheet หรือใช้ Python Pandas
   - กรองตามคอลัมน์ `category`, `topic_tags`, `research_track` (`USGS_REPLICATION`, `THAILAND_DATA`, `PDP2026_ENERGY_PLANNING`, `GENERAL_METHOD`, `PROJECT_INTERNAL`)
   - ตรวจสอบคอลัมน์ `evidence_status` (`SOURCE_VERIFIED`, `METADATA_ONLY`, `MISSING_LOCAL_FILE`)

2. **ทำความเข้าใจภาพรวมผ่าน Literature Map (`RESEARCH_MASTER_INDEX.md`)**:
   - สรุปความเชื่อมโยงของงานวิจัยกับ Pain Point ระดับประเทศ (PDP2026, Hyperscale Data Center)
   - สรุปกรอบทฤษฎี PFA, PU Learning, Spatial Validation, และ Environmental Screening

3. **นำรายการอ้างอิงไปใช้งาน (`10_SUPPLEMENTARY_AND_CITATIONS/geothermai_references.bib`)**:
   - มีไฟล์ BibTeX พร้อมสำหรับการจัดทำเอกสารวิชาการ รายงานการวิจัย หรือสไลด์นำเสนอ

---

## 3. หลักเกณฑ์ด้านลิขสิทธิ์และการใช้งานข้อมูล (License & Ethics)

- **COPY-ONLY Principle**: ไฟล์ทั้งหมดในคลังนี้ถูกคัดลอกมาจากต้นฉบับดั้งเดิม โดยไม่มีการแก้ไขเนื้อหา ไม่มีการลบ และไม่มีการย้ายไฟล์ต้นทาง
- **Restricted Local Use**: ไฟล์ PDF ที่มีลิขสิทธิ์ของสำนักพิมพ์ (Elsevier, Wiley) มีไว้สำหรับการศึกษาค้นคว้าภายในเครื่องของนักวิจัยเท่านั้น ห้ามนำขึ้น Public Git หรือแจกจ่าย
- **Fail-Closed Gate**: โครงการกำหนดให้โมเดลทำนายศักยภาพความร้อนใต้พิภพต้องปิดกั้นการทำงาน (Fail-Closed) ไว้ก่อน จนกว่าจะได้รับหนังสืออนุญาตเป็นลายลักษณ์อักษรจากกรมทรัพยากรธรณี (DMR) สำหรับการใช้ข้อมูลเชิงอนุพันธ์
