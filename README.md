# 🛰️ B73 Lead Radar

AI-assisted lead monitoring and qualification pipeline built for **B73 Digital Studio**.

It collects structured opportunities, stores them in SQLite, evaluates commercial intent using NVIDIA Nemotron, and surfaces qualified leads through Telegram.

---

## ✨ What It Does

```text
SOURCE
  ↓
COLLECT
  ↓
NORMALIZE
  ↓
DEDUPLICATE
  ↓
SQLITE
  ↓
AI QUALIFICATION
  ↓
TELEGRAM

 ```

The system is designed to separate actual buyer intent from low-value or irrelevant opportunities.

⚙️ Core Features

- Python-based modular pipeline
- SQLite persistence
- Duplicate-safe ingestion
- NVIDIA NIM integration
- Nemotron-powered lead qualification
- Telegram operator bot
- Manual lead ingestion
- Experimental EU TED procurement collector
- Environment-based secret management
- Modular collector architecture


🧠 AI Qualification

Default model:
nvidia/nemotron-3.5-lightning-30b-a3b
Optional deeper model:
nvidia/nemotron-3-ultra-550b-a55b
The qualifier evaluates signals such as:
- buyer intent
- commercial urgency
- scope clarity
- fixed-price suitability
- budget signals
- relevance to web/software development


   🧱 Architecture
  
                ┌──────────────┐
                │  Data Source │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │  Collector   │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Normalizer   │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Deduplication│
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │   SQLite     │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │  Nemotron AI │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │   Telegram   │
                └──────────────┘
  
🛰️ Telegram Commands

/start
/status
/analyze_new


🌍 EU TED Collector

The repository includes an experimental collector for the official EU TED procurement search API.
Current implementation demonstrates:
- official API integration
- query construction
- response parsing
- normalization into the internal Lead model
- SQLite ingestion
- duplicate-safe storage

  
The TED collector is included as a reference implementation and may require query tuning depending on the search scope and CPV filters.

🧪 Demo Lead

A demo lead can be added with:
python seed_test_lead.py
Then analyze it through Telegram:
/analyze_new

🚀 Installation

Clone the repository:
git clone https://github.com/fatihex3/b73-lead-radar.git
cd b73-lead-radar
Create a virtual environment:
python3 -m venv venv
source venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Create your environment file:
cp .env.example .env
Add your own credentials to .env.
Run:
python main.py

🔐 Security

Never commit:
- .env
- API keys
- Telegram tokens
- SQLite production databases
- SSH keys
- production logs
This repository contains no production credentials.

🛠️ Tech Stack

- Python
- SQLite
- Telegram Bot API
- NVIDIA NIM
- Nemotron
- HTTPX
- OpenAI-compatible API client

📌 Project Status

Public portfolio/reference release.
The production version contains additional reliability, observability, qualification and ingestion safeguards.

👨‍💻 Built by
B73 Digital Studio
https://b73.dev
