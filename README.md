# Low-Bandwidth Multilingual Telehealth Platform 🏥
### Powered by MediBridge (AI-Driven Backend Engine)

![FastAPI](https://img.shields.io/badge/FastAPI-0.129-009688?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?style=flat&logo=openai)
![IndicTrans2](https://img.shields.io/badge/AI4Bharat-IndicTrans2-FF6B35?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange?style=flat)
![Railway](https://img.shields.io/badge/Deployed-Railway-blueviolet?style=flat&logo=railway)

---

## 🌐 Live API
**Base URL:** `https://ruraltelehealthnlpbackend-production.up.railway.app`  
**API Docs:** `https://ruraltelehealthnlpbackend-production.up.railway.app/docs`

---

## 🌍 The Problem

India has 1.4 billion people. 65% live in rural areas.
And yet - the entire digital healthcare revolution has been built for urban India.

Here is the reality on the ground:

- 🗣️ A farmer in Bihar speaks Bhojpuri. The nearest specialist is in Delhi and speaks English.
- 👩‍⚕️ A tribal woman in Jharkhand speaks Santali. No telehealth app supports her language.
- 📶 A village in Rajasthan has 2G internet. Every existing telehealth platform buffers, crashes, or simply doesn't load.
- 📋 A rural ASHA worker fills patient forms in Hindi. The hospital system only accepts English records.

**Practo, 1mg, Apollo 247, Tata Health** - these platforms are excellent.
For urban India. For English speakers. For 4G users.

They were never designed for the 800 million who don't fit that profile.

**This platform is.**

---

## 💡 What We're Building - And Why It's Different

The **Low-Bandwidth Multilingual Telehealth Platform** is a healthcare
communication infrastructure built from the ground up for rural India.

At its core is **MediBridge** - a custom AI backend engine that does
something no existing telehealth platform in India currently offers:

> A patient speaks in their native Indian language.
> MediBridge transcribes it, translates it into English,
> and delivers it to a doctor, in real time & on a 2G connection.

That's the entire value proposition. Simple to explain. Incredible to build.
And we built it.

---

## 🆚 How We Stand Out Against Market Leaders

| Feature | Practo | 1mg | Apollo 247 | **Our Platform** |
|---------|--------|-----|------------|-----------------|
| Multilingual Voice Input | ❌ | ❌ | ❌ | ✅ 22 Languages |
| Low-Bandwidth Optimized | ❌ | ❌ | ❌ | ✅ Tested on 2G |
| AI Medical Translation | ❌ | ❌ | ❌ | ✅ IndicTrans2 |
| Rural-First Design | ❌ | ❌ | ❌ | ✅ Core Focus |
| DISHA Compliant Backend | ⚠️ | ⚠️ | ⚠️ | ✅ By Design |
| Open Source Backend | ❌ | ❌ | ❌ | ✅ GitHub |

The gap in the market is real. The technology to fill it now exists.
This platform connects the two.

---

## 🔬 The Novelty - What Makes This Genuinely New

Most telehealth platforms are booking systems with a video call bolted on.
We are building a **language infrastructure layer** for Indian healthcare.

Three things make this novel:

**1. IndicTrans2 in a Medical Context:**
IndicTrans2 by AI4Bharat is the most accurate Indic language translation
model available today, supporting all 22 scheduled Indian languages.
No production telehealth system currently uses it. We are integrating it
specifically for medical terminology, where accuracy isn't a nice-to-have,
it's life-critical.

**2. Whisper + IndicTrans2 Pipeline:**
OpenAI Whisper handles speech-to-text across Indian languages and accents
with remarkable accuracy. Chaining Whisper → IndicTrans2 into a single
real-time API pipeline is what MediBridge does. This specific pipeline
does not exist as a production healthcare tool anywhere currently.

**3. Low-Bandwidth as a Design Constraint, Not an Afterthought:**
Every architectural decision - payload size, API response structure,
audio compression - is made with a 2G connection in mind. We will document
and publish our bandwidth benchmarks openly. This is measurable, verifiable,
and reproducible by anyone.

---

## ⚙️ How It Works - Platform Workflow
```
PATIENT SIDE                    MEDIBRIDGE ENGINE                 DOCTOR SIDE
─────────────                   ─────────────────                 ───────────
Patient speaks          →       1. Audio received by FastAPI  →
in Tamil / Hindi /              2. Whisper transcribes audio
Bhojpuri / any of               3. IndicTrans2 translates          English text
22 Indian languages     →       4. Text stored in PostgreSQL  →    displayed to
via mobile interface            5. JWT-secured delivery            doctor in
                                6. Encrypted per DISHA             real time
```

**In simple terms:**
1. Patient opens app → taps microphone → speaks in their language
2. Audio sent to MediBridge backend via API
3. Whisper converts speech → text (in patient's language)
4. IndicTrans2 translates → English
5. Doctor sees clean English text of what patient said
6. Entire exchange stored securely, DISHA compliant

---

## 🏗️ MediBridge - Backend Architecture

MediBridge is the engine under the hood. Here's how it's structured:
```
medibridge-backend/
├── app/
│   ├── main.py            ← FastAPI server entry point
│   ├── routes/            ← All API endpoint definitions
│   │   ├── transcribe.py  ← Speech-to-text endpoints
│   │   ├── translate.py   ← Translation endpoints
│   │   ├── auth.py        ← Login, JWT token management
│   │   └── pipeline.py    ← Combined transcribe+translate
│   ├── models/            ← PostgreSQL database models
│   ├── services/          ← Core AI pipeline logic
│   │   ├── whisper_service.py  ← Whisper integration
│   │   └── translation_service.py ← Translation integration
│   └── utils/             ← Encryption, helpers, validators
├── tests/                 ← Full test suite
├── Procfile               ← Railway deployment config
├── runtime.txt            ← Python version for Railway
├── .env                   ← Environment variables (never committed)
├── requirements.txt       ← All dependencies
└── README.md
```

---

## 🛠️ Tech Stack - Every Choice Has a Reason

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend Framework | FastAPI (Python) | Async, fast, auto-docs, production-grade |
| Speech-to-Text | OpenAI Whisper | Best-in-class multilingual, handles Indian accents |
| Translation Engine | Google Translate via deep-translator | Fast, reliable, supports all Indian languages |
| Database | PostgreSQL | Reliable, ACID compliant, production standard |
| Authentication | JWT | Stateless, scalable, industry standard |
| Encryption | AES-256 | Medical data protection, DISHA requirement |
| Deployment | Railway | Fast, reliable cloud deployment |
| API Documentation | Swagger UI (built-in) | Auto-generated, always up to date |

---

## ⚡ Getting Started (Local Development)
```bash
# Clone the repository
git clone https://github.com/binnisha/Rural_Telehealth_NLP_Backend
cd Rural_Telehealth_NLP_Backend

# Create and activate environment
conda create -n medical-ai python=3.10
conda activate medical-ai

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with your DATABASE_URL and SECRET_KEY

# Run the server
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for local API documentation.

---

## 📊 Build Progress

| Phase | Description | Status |
|-------|-------------|--------|
| ✅ Phase 1 | Backend foundation, FastAPI server, core endpoints | Complete |
| ✅ Phase 2 | OpenAI Whisper integration, /transcribe endpoint | Complete |
| ✅ Phase 3 | Translation pipeline, /transcribe-and-translate | Complete |
| ✅ Phase 4 | PostgreSQL database, patient/doctor/consultation tables | Complete |
| ✅ Phase 5 | JWT authentication, role-based access, doctor verification | Complete |
| ✅ Phase 6 | Railway deployment, live API | Complete |
| ✅ Phase 7 | AES-256 encryption, DISHA compliance | Complete |
| ✅ Phase 8 | Performance testing, bandwidth benchmarking | Complete |

---

## 🔒 Compliance & Security

This platform is being built with **DISHA (Digital Information Security
in Healthcare Act)** compliance as a core requirement, not an afterthought:

- All patient data encrypted at rest using AES-256
- All data in transit secured via TLS
- Role-based access control - patients and doctors see only what they should
- No patient data stored without explicit consent flows
- Full audit trail of all consultations
- Doctor verification system — unverified doctors cannot access patient data

---

## 📄 License
MIT License - see LICENSE file for details