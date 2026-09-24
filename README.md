# 🛰️ B73 Lead Radar

AI-assisted lead qualification and monitoring pipeline built for
B73 Digital Studio.

The project collects structured opportunities, removes duplicates,
stores them in SQLite, evaluates commercial intent using NVIDIA NIM,
and surfaces qualified opportunities through Telegram.

## Features

- Python-based lead pipeline
- SQLite persistence
- Duplicate protection
- NVIDIA NIM integration
- Nemotron lead qualification
- Telegram operator bot
- Manual lead ingestion
- Environment-based secret management
- Modular collector architecture

## Architecture

```text
COLLECT
   ↓
NORMALIZE
   ↓
DEDUPLICATE
   ↓
AI QUALIFICATION
   ↓
STORE
   ↓
TELEGRAM
