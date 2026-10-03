# LiftMate — AI Hybrid Athlete Performance & Telemetry OS

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-208%20Passed-4ff7a8?style=flat-square&logo=pytest&logoColor=black)](tests/)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-black?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![Strava API](https://img.shields.io/badge/Integrations-Strava%20v3-FC5200?style=flat-square&logo=strava&logoColor=white)](https://strava.com)
[![Telegram](https://img.shields.io/badge/Bot-Telegram%20API-2CA5E0?style=flat-square&logo=telegram&logoColor=white)](https://telegram.org)

**LiftMate** is an athletic telemetry and AI coaching platform engineered for **hybrid athletes** who combine heavy resistance training with endurance running.

By fusing pure-Python deterministic arithmetic (e1RM, ACWR, HR zones, session density) with a multi-agent Google Gemini intelligence engine, LiftMate eliminates LLM hallucinations on numbers while delivering deep biomechanical insights, automated Telegram workout briefings, and a modern dark-mode web dashboard.

---

## Key Highlights

- **Zero-Hallucination Math Principle**: All numbers (tonnage, rep-max formulas, aerobic decoupling, ACWR, heart rate zones, push/pull ratios) are computed deterministically in pure Python before the AI ever sees them. The LLM only interprets already-computed telemetry.
- **Dual-Channel Experience**: Full athletic SaaS Web Dashboard (responsive desktop/mobile) paired with instantaneous Telegram messaging ([@sujal_liftmate_bot](https://t.me/sujal_liftmate_bot)).
- **Multi-Agent Gemini Architecture**: Specialized reasoning agents (Strength Analyst, Endurance Analyst, Chart Agent, Conversational Coach) coordinated by a lightweight orchestrator with 30-minute conversational session memory.
- **Serverless & Event-Driven**: Designed for Vercel with an asynchronous QStash queue ensuring sub-200ms webhook acknowledgments and background worker execution.

---

## System Architecture

```
                    ┌────────────────────────────────────────────────────────┐
                    │                      DATA INGEST                       │
                    └────────────────────────────────────────────────────────┘
                      ▲                                      ▲
                      │ Webhook (<200ms ACK)                 │ Webhook (<200ms ACK)
               ┌──────────────┐                       ┌──────────────┐
               │  Strava API  │                       │ Telegram Bot │
               └──────────────┘                       └──────────────┘
                      │                                      │
                      └──────────────────┬───────────────────┘
                                         ▼
                             ┌───────────────────────┐
                             │ Upstash QStash (Queue)│
                             └───────────────────────┘
                                         │
                                         ▼
                    ┌────────────────────────────────────────┐
                    │         /api/worker (The Brain)        │
                    ├────────────────────────────────────────┤
                    │ • Event Log & Idempotency Filter       │
                    │ • Token Cipher (Fernet Encrypted)      │
                    │ • Redis Ephemeral State (30-min window)│
                    └────────────────────────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
     ┌────────────────────────┐                     ┌────────────────────────┐
     │   Pure-Python Engine   │                     │ Multi-Agent Gemini LLM │
     ├────────────────────────┤                     ├────────────────────────┤
     │ • Epley / Brzycki 1RM  │                     │ • Orchestrator Agent   │
     │ • Push / Pull Balances │                     │ • Strength Analyst     │
     │ • ACWR Workload Ratio  │                     │ • Endurance Analyst    │
     │ • Pa:HR Decoupling     │                     │ • Interactive Coach    │
     │ • 20 Matplotlib Charts │                     │ • Chart Selector       │
     └────────────────────────┘                     └────────────────────────┘
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         ▼
                    ┌────────────────────────────────────────┐
                    │               INTERFACES               │
                    ├────────────────────┬───────────────────┤
                    │   Web Dashboard    │   Telegram Bot    │
                    │ (Edge CDN / WSGI)  │ (HTML Render/Push)│
                    └────────────────────┴───────────────────┘
```

---

## Core Capabilities

### 1. Unified Web Dashboard
- **Overview & KPIs**: Live tracking of weekly volume ($kg$), endurance mileage ($km$), Acute:Chronic Workload Ratio (ACWR), and verified PRs.
- **AI Advisor Studio**: Context-aware chat with Coach LiftMate featuring pre-built athletic prompts and 1-click **"Forward to Telegram"** options.
- **Workouts Feed & Detail Drawer**: Interactive activity breakdown displaying working sets, load, RPE, splits, heart rate zone progress, and AI briefings.
- **Personal Records Trophy Board**: Filterable leaderboards across all tracked compound lifts (Chest, Legs, Shoulders, Back).
- **Telemetry Analytics Studio**: Interactive viewer for 20 deterministic Matplotlib visual chart presets.
- **Workout Lab & Simulator**: Test and validate synced Hevy/Strava workout logs with live volume, push/pull ratio, session density, and instant Telegram dispatch.
- **Integrations Control Center**: 1-click Strava OAuth connect, live Telegram test pings, weekly digest dispatch, and profile baseline tuning.

### 2. Pure-Python Deterministic Metric Engines
- **Strength Telemetry** (`app/metrics/strength.py`):
  - Dual 1RM calculation: **Epley** vs. **Brzycki** with automated divergence flags ($>5\%$ disagreement).
  - Push/Pull and Upper/Lower mechanical balance ratios.
  - Session Density ($kg/min$) and total working set counts (warmups automatically filtered out).
  - Rep-range classification: Strength ($\le 5$), Hypertrophy ($6-12$), Endurance ($13+$).
  - Bilateral dumbbell tonnage doubling logic.
- **Endurance Telemetry** (`app/metrics/endurance.py`):
  - Lactate Threshold HR (LTHR) and 5-zone time distribution with second-by-second duration weighting.
  - Aerobic Decoupling ($Pa:HR$ efficiency factor drift between first and second half).
  - Banister TRIMP (Training Impulse) calculation.
- **Cross-Discipline Fatigue** (`app/metrics/acwr.py`):
  - Acute:Chronic Workload Ratio (7-day acute vs. 28-day chronic exponential load).
  - Fatigue categorization: Under-training ($<0.8$), Optimal Sweet Spot ($0.8-1.3$), Elevated Injury Risk ($>1.5$).

### 3. Analytics Studio — 20 Preset Matplotlib Charts
- **Strength**: S01 Volume by Muscle, S02 Volume Progression, S03 e1RM Trend, S04 Set Breakdown, S05 Session vs. Last, S06 Weekly Sets vs. Target, S07 Rep-Range Mix, S08 PR Timeline.
- **Endurance**: E01 HR Zone Distribution, E03 Pace & HR Dual Stream, E04 Kilometer Splits Bar, E05 Aerobic Decoupling, E07 Weekly Volume by Zone, E08 80/20 Polarized Mix, E09 Cadence Over Time, E10 Elevation & HR Profile.
- **Cross-Discipline**: X01 ACWR Timeline, C02 ACWR Gauge, C03 Training Split Hours, X02 12-Week Consistency Heatmap Calendar.

---

## Repository Structure

```
strava-trainer/
├── api/
│   └── index.py               # WSGI Python entrypoint for Vercel & local server
├── app/
│   ├── agents/                # Multi-agent Gemini orchestrator, analysts & coach
│   ├── charts/                # 20 Matplotlib Agg chart preset generators
│   ├── clients/               # Strava, Telegram, and Gemini API clients
│   ├── config.py              # Pydantic Settings environment configuration
│   ├── memory/                # Ephemeral conversation state & sliding window
│   ├── metrics/               # Pure-Python deterministic strength & endurance engines
│   ├── models/                # Pydantic schemas (Workout, Streams, Enums)
│   ├── parsers/               # Hevy Strava description parser
│   ├── platform/              # HTTP adapters and dependency-injection wiring
│   ├── prompts/               # Versioned Markdown prompts for Gemini agents
│   ├── render/                # Telegram HTML sanitization & chunking
│   ├── security/              # Fernet crypto cipher & QStash JWT validation
│   ├── storage/               # Postgres (Database) & Upstash Redis adapters
│   └── web/                   # Transport-agnostic handlers (frontend, webhooks, cron)
├── frontend/                  # Web dashboard source (HTML, CSS, Vanilla JS)
├── public/                    # Edge CDN static distribution directory
├── migrations/                # Durable SQL schema migrations (Postgres)
├── scripts/                   # CLI utilities (OAuth bootstrap, webhooks, backfill)
├── tests/                     # 208 comprehensive unit tests
├── pyproject.toml             # Python build configuration and dependencies
├── vercel.json                # Vercel deployment, serverless functions & cron config
└── run.py                     # Local development WSGI runner (port 3000)
```

---

## Local Development & Setup

### 1. Prerequisites
- **Python 3.12+**
- **Git**
- **Credentials**:
  - [Telegram Bot](https://t.me/BotFather) token & your numeric Chat ID (from [@userinfobot](https://t.me/userinfobot))
  - [Strava API Application](https://www.strava.com/settings/api) (Client ID & Client Secret)
  - [Google Gemini API Key](https://aistudio.google.com/apikey)
  - [Upstash Redis & QStash](https://upstash.com) credentials
  - [Neon](https://neon.tech) or [Supabase](https://supabase.com) Postgres database URL

### 2. Environment Configuration
Create a `.env` file in the project root:
```bash
cp .env.example .env
```
Populate `.env` with your credentials:
```ini
STRAVA_CLIENT_ID=your_strava_client_id
STRAVA_CLIENT_SECRET=your_strava_client_secret
STRAVA_ATHLETE_ID=your_athlete_id
STRAVA_VERIFY_TOKEN=random_verification_string
GEMINI_API_KEY=your_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_OWNER_CHAT_ID=your_numeric_chat_id
TELEGRAM_WEBHOOK_SECRET=random_telegram_secret
DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require
UPSTASH_REDIS_REST_URL=https://your-redis.upstash.io
UPSTASH_REDIS_REST_TOKEN=your_upstash_redis_token
QSTASH_TOKEN=your_qstash_token
QSTASH_CURRENT_SIGNING_KEY=your_qstash_current_key
QSTASH_NEXT_SIGNING_KEY=your_qstash_next_key
INTERNAL_API_SECRET=your_internal_secret_hex_32
ENCRYPTION_KEY=your_fernet_32_byte_base64_key
APP_URL=http://localhost:3000
```

Generate local cryptographic secrets:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" # -> ENCRYPTION_KEY
python -c "import secrets; print(secrets.token_hex(32))"                                   # -> INTERNAL_API_SECRET
```

### 3. Installation & Database Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (Postgres)
python -c "from pathlib import Path; from app.config import get_settings; from app.storage.db import Database; Database(get_settings().database_url).apply_migrations(Path('migrations'))"
```

### 4. Running the Application
```bash
python run.py
```
Open [http://localhost:3000](http://localhost:3000) in your browser to access the dashboard.

---

## Testing

The test suite covers the entire deterministic pipeline, parser edge-cases, cryptographic token ciphering, QStash JWT signature verification, and agent prompt pipelines without requiring external network calls.

```bash
# Run all unit tests
pytest -q

# Run specific domain tests
pytest tests/test_metrics_strength.py
pytest tests/test_metrics_endurance.py
pytest tests/test_parser_hevy_strava_description.py
```

---

## Deployment on Vercel

LiftMate is pre-configured for automated Vercel deployment:

1. **Import Project**: Push your code to GitHub and import the repository on [Vercel](https://vercel.com).
2. **Framework Preset**: Select **Other** (Vercel automatically detects `pyproject.toml` and `api/index.py`).
3. **Environment Variables**: Add all environment variables from `.env` to the Vercel project settings.
4. **Deploy**: Click **Deploy**. Vercel will install dependencies, host static assets on its Edge CDN from `public/`, and deploy the serverless Python WSGI runtime.
5. **Post-Deployment Webhooks**:
   - Update `APP_URL` in Vercel to your live production domain (e.g. `https://your-domain.vercel.app`).
   - Run the Telegram webhook registration script:
     ```bash
     python scripts/setup_telegram_webhook.py set
     ```
   - In Strava Developer Settings, set the **Authorization Callback Domain** to your Vercel domain.
   - Register the Strava push subscription:
     ```bash
     python scripts/setup_strava_webhook.py create
     ```
   - Copy the returned subscription ID to `STRAVA_SUBSCRIPTION_ID` in Vercel.

---

## Security & Privacy

- **Data Encryption**: All athlete OAuth tokens stored in Postgres are encrypted using Fernet (AES-128-CBC + HMAC-SHA256).
- **Constant-Time Verification**: Authorization headers and webhook signatures are compared using constant-time string comparisons to eliminate timing attacks.
- **Edge Queue Security**: Inbound worker requests validate Upstash QStash HS256 signatures with support for zero-downtime key rotation.
- **Strict Privacy**: Telemetry arithmetic executes locally on your compute. Only structured, pre-calculated metric summaries are passed to Google Gemini prompts.
