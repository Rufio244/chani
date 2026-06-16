# chani
🧠 CHANI - Semantic Intelligence Platform

CHANI (Cognitive Hybrid AI Network Intelligence) คือแพลตฟอร์ม AI ที่ออกแบบมาเพื่อรวมความสามารถของ AI หลายระบบเข้าด้วยกัน พร้อม Semantic Understanding, Memory, Reasoning และ Agent Integration ภายใต้ API เดียว

---

🚀 Features

🤖 Multi-AI Gateway

รองรับการเชื่อมต่อ AI หลายระบบ

- OpenAI
- Gemini
- Future Models
- Local Models (Coming Soon)

🧠 Semantic Core

แปลงภาษามนุษย์เป็น Concept กลาง

ตัวอย่าง

Input

ฉัน ดื่ม น้ำ

Output

{
  "semantic": [
    {
      "id": "SEM-000001",
      "concept": "SELF"
    },
    {
      "id": "ACT-000001",
      "concept": "DRINK"
    },
    {
      "id": "OBJ-000001",
      "concept": "WATER"
    }
  ]
}

🔑 API Key System

- User Registration
- API Key Generation
- Access Control

📚 Memory System

จัดเก็บ

- Chat History
- Semantic History
- Learned Skills
- Usage Logs

#AGI Gateway

รองรับคำสั่งแบบ

#AGI วิเคราะห์ตลาด AI

{
  "intent": "ANALYZE",
  "target": "AI_MARKET"
}

---

📦 Installation

Clone Repository

git clone https://github.com/Rufio244/chani.git

cd chani

Create Virtual Environment

python -m venv venv

source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

---

🔐 Environment Variables

สร้างไฟล์

.env

ตัวอย่าง

OPENAI_API_KEY=YOUR_OPENAI_KEY
GEMINI_API_KEY=YOUR_GEMINI_KEY

---

▶️ Run Locally

uvicorn chani:app --host 0.0.0.0 --port 10000

เปิด

http://localhost:10000

---

🐳 Docker

Build

docker build -t chani .

Run

docker run -p 10000:10000 \
-e OPENAI_API_KEY=YOUR_OPENAI_KEY \
-e GEMINI_API_KEY=YOUR_GEMINI_KEY \
chani

---

🌐 API Endpoints

Health Check

GET /health

Response

{
  "status": "online"
}

---

Chat

POST /v1/chat

Request

{
  "message": "สวัสดี Chani"
}

Headers

Authorization: Bearer YOUR_API_KEY

---

Semantic Parser

POST /semantic/parse

Request

{
  "text": "ฉัน ดื่ม น้ำ"
}

---

AGI Gateway

POST /agi

Request

{
  "text": "#AGI วิเคราะห์ตลาด AI"
}

---

Dashboard

GET /dashboard

---

🏗 Architecture

User
 │
 ▼
CHANI Gateway
 │
 ├── Authentication
 ├── API Keys
 ├── Semantic Core
 ├── Memory
 ├── AGI Gateway
 │
 ▼
Multi-AI Layer
 │
 ├── OpenAI
 ├── Gemini
 └── Future Models
 │
 ▼
Reasoning
 │
 ▼
Response

---

🛣 Roadmap

v1

- FastAPI
- API Keys
- OpenAI Integration
- Semantic Parser
- Dashboard

v2

- Persistent Memory
- SQLite/PostgreSQL
- Semantic Search
- Knowledge Graph

v3

- Reasoning Engine
- Agent System
- Face Auto Integration
- Indow Integration
- Dola Integration

v4

- Autonomous Learning
- Distributed Agent Network
- Semantic Intelligence Hub

---

📜 License

MIT License

---

👨‍💻 Author

Rufio244

CHANI Semantic Intelligence Platform
