# GeoThermAI Local Research Library — Handoff

ไฟล์ `MASTER_PROMPT_LOCAL_RESEARCH_COLLECTION.md` เป็นคำสั่งสำหรับ AI Coding Agent / Codex **ที่รันบนเครื่อง Local ของผู้ใช้** ให้ค้นหาและจัดระเบียบไฟล์อ้างอิงที่มีอยู่แล้วโดยไม่แก้ไขต้นฉบับ

`REFERENCE_CHECKLIST.csv` เป็นรายการเอกสารเป้าหมาย ไม่ใช่รายงานยืนยันว่าไฟล์เหล่านั้นมีอยู่บนเครื่อง ผู้ใช้หรือ Codex ต้องทำ Local Inventory จริงก่อน

วิธีใช้:
1. เปิด GeoThermAI Repository ใน Codex หรือ Agent ที่มีสิทธิ์อ่านไฟล์ Local
2. ส่งเนื้อหาไฟล์ Master Prompt ให้ Agent
3. ตรวจว่า Working Directory เป็น GeoThermAI Repo ที่ต้องการ
4. ให้ Agent รันรวบรวมตามขั้นตอน แล้วอ่าน `research_library/00_INDEX/` และ Execution Log

เน้น Copy-only, SHA-256, Citation/License Audits, and no automatic web downloads.
