# Phase 2F: การตรวจสอบเชิงวิทยาศาสตร์และลำดับงานที่ต้องปลดล็อก

**วันที่** 27 ตุลาคม 2569 | **การตัดสิน:** NO-GO FOR PREDICTIVE ML | **เป้าหมาย:** Geothermal Prospectivity Prediction สำหรับพื้นที่นำร่องประเทศไทย

## ผลที่มีหลักฐานจากรายงาน (ไม่ใช่การตรวจ repo ใหม่)
- Phase 2E รายงานว่าได้เตรียมสถาปัตยกรรม Prediction, แยก Train-Only Scaling และป้องกัน target-derived features พร้อม Python 41, web 25, unittest 4 ผ่านแล้ว แต่ไม่มี source tree ที่จะพิสูจน์ซ้ำในเซสชันนี้
- Registry จำนวน 47 rows: 14 internally consistent map points, 31 provisional south, 2 withheld. **ไม่ใช่ 47 independent positive labels**; รายงานคาด ~6–10 ระบบในภาคเหนือแต่ยังไม่มีผู้เชี่ยวชาญรับรอง
- Northern DMR geology 1,266 polygons/42 symbols: contextual use; สิทธิ์ใช้ฝึกและ derivative release ยังต้องยืนยัน
- Active fault geometry local 630 เส้น: ยังถูกบล็อกด้วยเงื่อนไขสิทธิ์; live DMR structure query ไม่มี geometry
- Terrain SRTM มี 5 tiles เท่านั้น; coverage ไม่ต่อเนื่องตาม AOI ผู้วิจัยต้องกำหนดจริง
- IHFC 154 measurements ที่ 111 พิกัด: **observed points only**; ห้ามอ้างว่า surface heat-flow ปะติดปะต่อหรือใช้ train ได้
- Landsat ST raster 0 files valid; gravity study south 2026 เป็น lead ไม่ใช่ datasets ที่พร้อมใช้

## งานที่ทำต่อได้โดยไม่ฝืนฝึกโมเดล
1. จัด **expert label adjudication packet**: ระบุ published record ID, parent hydrothermal system, evidence grade, coordinate quality, source and reason; ขอ geologist ลงนามการ grouping และ withheld policy
2. เลือก **pilot AOI** โดยเปรียบเทียบ spatial overlap ที่มีจริง, label group independence, data licensing and resolution; พิกัด Northern AOI จาก Phase 2E เป็น candidate เท่านั้น ไม่ใช่การอนุมัติ
3. ขอหนังสือชี้แจง DMR ครอบคลุมดาวน์โหลดประมวลผล, ML derivatives, commercial potential, publication, และ geodata redistribution โดย **ไม่เปลี่ยน license flags** จนได้คำตอบ
4. เติม DEM **เฉพาะช่องโหว่** หลังล็อก AOI; ดาวน์โหลดผ่านช่องทาง USGS/NASA ที่เป็นทางการ, verify checksum/CRS/footprints
5. Preregister PU sampling, buffer sensitivity, expert grouping holdouts, test design, metrics and failure reporting; ถ้ากลุ่มอิสระน้อยเกิน ให้รายงานว่าไม่สามารถประเมินทั่วไปได้
6. ใช้ USGS 2023 public release เพื่อ *วางแผน* replication บนต่างประเทศแยกโดยเด็ดขาดจากโมเดลไทย เมื่อดาวน์โหลดจริงแล้วค่อยรายงาน reproducibility

## ผ่าน Phase 2F เมื่อใด
ต้องมีชุดเอกสาร sign-off จริงสำหรับ labels/groups, locked AOI, datasets legally cleared & spatially intersecting, PU protocol, validation and external test, independent group adequacy, output rights; ตรวจสอบใน 9-condition gate. หากข้อใดไม่ผ่าน = ยัง NO-GO. รายละเอียดใน `phase2f_gate_snapshot.json`.

## สิ่งที่ห้ามอ้าง
ไม่มี Thai model accuracy/F1/AUC; ไม่มี Thai predictive map, drilling success, MW, saved cost หรือ heatflow interpolation. Test ผ่านเป็นหลักฐาน code behavior ไม่ใช่ prediction accuracy.
