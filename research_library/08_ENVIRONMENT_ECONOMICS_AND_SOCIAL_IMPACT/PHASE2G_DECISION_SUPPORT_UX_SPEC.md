# ข้อกำหนดการออกแบบส่วนต่อประสานผู้ใช้เพื่อสนับสนุนการตัดสินใจสำรวจ (Phase 2G)
**GeoThermAI Evidence-Based Exploration Decision Support UX Specification**  
*วันที่: 29 ตุลาคม 2569 | โครงการ GeoThermAI (CoreX) | ฝ่ายออกแบบประสบการณ์ผู้ใช้และวิศวกรรมฟรอนต์เอนด์*

---

## 1. ปรัชญาการออกแบบและคำถามหลัก 4 ข้อ (Core UX Philosophy)

ระบบสนับสนุนการตัดสินใจสำรวจความร้อนใต้พิภพ (Exploration Decision Support System) ใน GeoThermAI ถูกออกแบบมาเพื่อตอบคำถามเชิงยุทธศาสตร์ 4 ข้อ ของนักธรณีวิทยา ผู้บริหารแผนพลังงาน และนักลงทุน โดยไม่จำเป็นต้องพึ่งพาโมเดลปัญญาประดิษฐ์ที่ยังไม่ผ่านเกณฑ์รับรอง:

```
[คำถามที่ 1: ควรสำรวจพื้นที่ใดก่อน?]
└── ลำดับความสำคัญในการสำรวจ (Exploration Priority Tier: Tier A ถึง Tier E)

[คำถามที่ 2: ทำไมจึงควรสำรวจพื้นที่นี้?]
└── เหตุผลทางธรณีวิทยาและหลักฐานเชิงประจักษ์ (อุณหภูมิผิวดิน, ธรณีเคมี, โครงสร้างรอยเลื่อน)

[คำถามที่ 3: หลักฐานมีความน่าเชื่อถือเพียงใด?]
└── ระดับความน่าเชื่อถือของแหล่งที่มา (Provenance Tier), คุณภาพพิกัด, ช่องว่างของข้อมูล

[คำถามที่ 4: ต้องดำเนินการสำรวจภาคสนามอะไรต่อ?]
└── แผนที่นำทางการสำรวจภาคสนาม (Actionable Field Investigation Roadmap)
```

---

## 2. โครงสร้างส่วนประกอบหน้าจอ (UI Architecture & Wireframes)

ระบบประกอบด้วย 4 โมดูลหลักที่ทำงานสอดประสานกันบนหน้าจอแผนที่เชิงโต้ตอบ (Evidence Explorer):

```
+----------------------------------------------------------------------------------------------------+
| GeoThermAI Evidence Explorer v0.3 (Phase 2G)                 [Language: TH | EN] [Status: NO-GO]   |
+------------------------------------+---------------------------------------------------------------+
| PANEL A: EVIDENCE INSPECTOR        | PANEL B: INTERACTIVE EVIDENCE MAP                             |
| - Layer Provenance & License       |                                                               |
| - Geodesic Spatial Coverage (33.8%)|   [Maplibre GL Engine - WGS84 EPSG:4326]                     |
| - Missing SRTM Tiles (7 missing)   |   * 14 Consistent Hot Spring Points                           |
| - DMR Fault WFS Status: BLOCKED    |   x 2 Withheld Discrepant Points                              |
| - ML Gate Status: FAIL-CLOSED      |   ? 31 Provisional Southern Points                            |
|                                    |   --- Layer Overlays:                                         |
+------------------------------------+       [x] DMR 1:250k Lithology Polygons                       |
| PANEL C: ENVIRONMENTAL SCREENING   |       [ ] IHFC Heat Flow Borehole Points (Descriptive Only)    |
| - DNP National Parks (Sec. 19)     |       [x] Environmental Exclusion Overlay (DNP / WSC 1A)      |
| - Cabinet Watershed (Class 1A/1B/2)|       [ ] Prospective Heatmap (DISABLED - ML GATE LOCKED)     |
| - RFD Forest Reserves (Sec. 16)    |                                                               |
+------------------------------------+---------------------------------------------------------------+
| PANEL D: EXPLORATION DECISION CARD & FIELD ROADMAP (Selected: Mae Chan System)                     |
| Priority: TIER_A_HIGH_EVIDENCE_FEASIBLE | Env: CONDITIONAL_REVIEW (Outside National Park)           |
| Geologic Rationale: Triassic biotite granites intersected by ENE-trending Mae Chan active fault   |
| Surface Temp: 99.1°C | Estimated Reservoir Temp: 140-150°C (Quartz Fournier 1977)                 |
| Actionable Next Steps:                                                                             |
| 1. [ACTION] 3D Magnetotelluric (MT) resistivity survey to map clay cap (smectite) boundary        |
| 2. [ACTION] Shallow temperature gradient drilling (<300m) to confirm conductive heat flow        |
| 3. [ACTION] Municipal and community land tenure consultation (Outside DNP park)                   |
+----------------------------------------------------------------------------------------------------+
```

---

## 3. รายละเอียดการทำงานของแต่ละแผงควบคุม (Component Specifications)

### แผงควบคุม A: ตัวตรวจสอบหลักฐาน (Evidence Inspector Panel)
- **วัตถุประสงค์:** แสดงที่มา คุณภาพ และข้อจำกัดของข้อมูลทุกชั้น
- **ตัวชี้วัดที่ต้องแสดง:**
  1. `Provenance Tier`: TIER_1 (หน่วยงานทางการโดยตรง), TIER_2 (บทความวิชาการผ่านการประเมิน), TIER_3 (ฐานข้อมูลสากล), TIER_4 (ข้อมูลชั่วคราว), TIER_5 (ข้อมูลถูกระงับ)
  2. `Geodesic Coverage Pct`: แสดงเปอร์เซ็นต์พื้นที่จริงที่ครอบคลุมในเขตศึกษาภาคเหนือ (102,125.39 ตร.กม.)
  3. `Missing Components Warning`: แสดงรายการชิ้นส่วนที่ยังขาดหายอย่างโปร่งใส เช่น "ขาดข้อมูล DEM 7 ระวาง" หรือ "บริการ WFS รอยเลื่อนของ กรมทรัพยากรธรณี ส่งคืน 0 รูปทรง"

### แผงควบคุม B: แผนที่เชิงโต้ตอบพร้อมเกราะป้องกันความผิดพลาด (Fail-Closed Map)
- **การแสดงผลจุดน้ำพุร้อน:**
  - จุดสีเขียว: พิกัดผ่านการตรวจสอบความสอดคล้อง (<100 ม.) จำนวน 14 จุด
  - จุดสีแดงกากบาท: พิกัดถูกระงับเนื่องจากคลาดเคลื่อนเกิน 1 กม. (CR_02) หรือขาดพิกัดลิปดา (CM_16)
  - จุดสีส้มมีเครื่องหมายคำถาม: พิกัดชั่วคราวภาคใต้ 31 จุด (รอการพิสูจน์ทราบโซน UTM)
- **การล็อกการทำงานของ AI (Runtime Guardrails):**
  - สวิตช์เปิดชั้นข้อมูล `Prospective Heatmap` จะถูกปิดใช้งาน (Disabled)
  - เมื่อนำเมาส์ไปชี้ (Hover) จะแสดงข้อความเตือน: `"การสร้างแผนที่ความน่าจะเป็นถูกระงับตามเกณฑ์ทางวิทยาศาสตร์ (ML Gate Status: NO_GO_FOR_PREDICTIVE_ML) เนื่องจากข้อมูลตัวแปรและป้ายกำกับยังไม่ผ่านการรับรองอย่างเป็นทางการ"`

### แผงควบคุม C: ตัวคัดกรองสิ่งแวดล้อม (Environmental Screening Overlay)
- **การจำแนกสีแสดงผลเชิงพื้นที่:**
  - สีแดงโปร่งแสง: `CRITICAL_EXCLUSION` (เขตอุทยานแห่งชาติ, ป่าต้นน้ำชั้น 1A)
  - สีเหลืองโปร่งแสง: `CONDITIONAL_REVIEW` (ป่าสงวนแห่งชาติ, ส.ป.ก., ลุ่มน้ำชั้น 1B/2)
  - สีน้ำเงินโปร่งแสง: `MONITORED_FEASIBILITY` (พื้นที่ชุมชน, ระยะแนวสายส่งไฟฟ้า)
- **การแจ้งเตือนสิทธิการใช้ที่ดิน:** เมื่อคลิกเลือกจุดน้ำพุร้อน ระบบจะแสดงสถานะการซ้อนทับด้านสิ่งแวดล้อมทันที เช่น `"โป่งน้ำร้อนฝาง: ตั้งอยู่ในเขตอุทยานแห่งชาติดอยผ้าห่มปก ห้ามการขยายกำลังผลิตเชิงพาณิชย์ตาม มาตรา 19"`

### แผงควบคุม D: การ์ดสรุปการตัดสินใจและแผนสำรวจภาคสนาม (Exploration Decision Card)
- **ระดับความสำคัญในการสำรวจ (Priority Tiers):**
  - **Tier A (High Evidence, Feasible):** ข้อมูลชัดเจน พิกัดถูกต้อง อยู่นอกเขตอุทยานฯ (เช่น แม่จัน/ป่าตึง) $\rightarrow$ มีความคุ้มค่าสูงสุดในการลงทุนสำรวจขั้นถัดไป
  - **Tier B (High Evidence, Environmentally Constrained):** ศักยภาพความร้อนสูง แต่ติดข้อจำกัดทางกฎหมายอุทยานฯ (เช่น ฝาง, ป่าแป๋) $\rightarrow$ จำกัดเฉพาะงานวิจัยทางวิชาการ ห้ามเจาะเชิงพาณิชย์
  - **Tier C (Moderate Evidence, Data Gaps):** มีน้ำพุร้อน แต่ขาดข้อมูลธรณีเคมีและแบบจำลองโครงสร้าง $\rightarrow$ ต้องเก็บตัวอย่างน้ำเพื่อวิเคราะห์ไอโซโทปก่อน
  - **Tier D (Provisional Coordinates):** พิกัดชั่วคราวภาคใต้ $\rightarrow$ ต้องส่งทีมรังวัด GPS ภาคสนาม
  - **Tier E (Withheld):** พิกัดคลาดเคลื่อนร้ายแรง $\rightarrow$ ระงับการนำเข้าสู่กระบวนการวางแผน
- **แผนปฏิบัติการภาคสนามที่แนะนำ (Actionable Roadmap):** แสดงขั้นตอนงานสำรวจทางธรณีฟิสิกส์และธรณีเคมีที่จำเป็นในลำดับถัดไปอย่างเป็นรูปธรรม เช่น การทำ Magnetotelluric (MT), การเจาะหลุมวัดเกรเดียนต์ความร้อนตื้น (<300 ม.), การสำรวจแนวสัมผัสรอยเลื่อน
