AI Agent & Chatbot Backend Services

Welcome to the backend repository for our AI Agent and Chatbot platform. This document serves as the central engineering guide for understanding the system architecture, component responsibilities, and local development workflows.

Our backend is designed to handle high-concurrency, asynchronous chat sessions, reliable background task scheduling, and secure data persistence.
Features

    Asynchronous Chat Session Management: Event-driven architecture to handle concurrent, real-time client-agent interactions without blocking the main event loop.

    Robust Task Scheduling: Distributed message queues to manage long-running background jobs, retries, and scheduled tasks.

    Automated Reporting Pipeline: Scheduled worker systems that compile system/lead metrics into Excel reports and distribute them daily.

    Secure Data Multi-Tenancy: Isolated storage of client configurations, agent prompts, and sensitive lead data.

## Features

- **Asynchronous Processing:** Powered by FastAPI and Uvicorn for high-throughput capability.
- **Strict Validation:** Uses Pydantic schemas to sanitize and gate incoming data.
- **Background Jobs:** Integrated with Celery and Redis to handle heavy lifting (Excel generation, emails) without blocking the API.
- **Docker Ready:** Complete multi-container setup (API, Celery, Redis, Postgres, and Mailpit for local email testing).
- **Free Notifications:** Routes alerts via standard SMTP or Discord/Telegram Webhooks, bypassing paid services like SendGrid.
- **Admin Management:** Dedicated routes to handle business logic like setting office hours or custom bot preferences.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.10+ | Core Programming Language |
| FastAPI | Web Framework (Async API Endpoints) |
| PostgreSQL | Relational Database for Leads & Client Configs |
| Celery + Redis | Distributed Task Queue & Message Broker |
| Mailpit | Local, offline SMTP testing server |
| Pydantic | Data Serialization & Schema Validation |
| Docker & Compose | Containerization & Local Orchestration |

---

## Project Structure

```text
bulkhead-bot-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app initialization & CORS setup
│   ├── api/                   # API Endpoints
│   │   ├── __init__.py
│   │   ├── routes_chat.py     # Handles incoming bot messages/payloads
│   │   └── routes_admin.py    # Endpoints for companies to set hours/preferences
│   ├── core/                  # Configuration
│   │   ├── config.py          # Environment variables (DB URIs, SMTP hosts)
│   │   └── security.py        # API key verification for widget requests
│   ├── db/                    # Database setup
│   │   ├── session.py         # Postgres connection logic
│   │   └── models.py          # DB schemas (Client settings, Leads)
│   ├── schemas/               # Pydantic models for validation
│   │   ├── chat.py            # Validating incoming lead data
│   │   └── client.py          # Validating admin settings
│   ├── services/              # Business Logic
│   │   ├── excel_gen.py       # Logic to convert DB leads to Excel rows
│   │   ├── email_sender.py    # Native SMTP & Webhook notification logic
│   │   └── nlp_parser.py      # Extracts linear ft from raw text (optional)
│   └── tasks/                 # Background Jobs
│       ├── __init__.py
│       ├── celery_app.py      # Celery instance setup
│       └── daily_reports.py   # Scheduled task: fetch leads -> make Excel -> email
├── requirements.txt
├── .env                       # Secrets (ignored in git)
├── docker-compose.yml         # Spin-up API, Celery, Redis, Postgres, Mailpit
└── README.md
```

## High-Level Architecture Flow

   Frontend Widget
              │
              ▼
    [ main.py + security.py ] (CORS & Origin Guard)
              │
              ├──► /api/routes_admin.py ──► Admin Management
              │
              └──► /api/routes_chat.py
                        │
                        ▼ (Validates via schemas/chat.py)
                  [ db/session.py ] ──► Write to Postgres
                        │
                        ▼ (Triggers Async Task)
                  [ tasks/celery_app.py ]
                        │
                        └──► daily_reports.py ──► excel_gen.py ──► email_sender.py

### Local Development (Mailpit)
The `docker-compose.yml` file includes a lightweight mail server called **Mailpit**. When the Celery worker sends a daily report, Mailpit catches it locally. You can view the rendered emails and attachments at `http://localhost:8025` without needing an internet connection or real email addresses.

### Production Routing
The `email_sender.py` module supports two free production methods:
1.  **Standard SMTP:** Connects to any standard email provider (e.g., Gmail using an App Password) via Python's native `smtplib`.
2.  **Webhooks:** Pushes instant lead notifications to free platforms like Discord or Telegram, ideal for quick field-team alerts.

Local Development (With Docker)
-------------------------------
The easiest way to spin up the entire backend stack (Database, Cache, API, Workers, and Mail Testing) is using Docker Compose.

### 1\. Configure Environment Variables
Create a `.env` file in the root directory:
Code snippet
```
# Database Connections
DATABASE_URL=postgresql://user:password@db:5432/bulkhead_db
REDIS_URL=redis://redis:6379/0

# Mailpit Local Testing Ports
SMTP_HOST=mailpit
SMTP_PORT=1025
```

### 2\. Spin Up the Containers
Bash
```
docker-compose up --build
```
This single command handles setting up PostgreSQL, Redis, Mailpit, running the FastAPI server on port `8000`, and spinning up the independent Celery worker instance.

### 3\. Review Dashboards
Once running, you can access the following local interfaces:
-   **FastAPI Interactive Docs:** `http://localhost:8000/docs`
-   **Mailpit Email Interface:** `http://localhost:8025`

Development Roadmap
-------------------
### Phase 1 --- Environment & Shell Setup
-   [X] Initialize Git repository and structure folder modules.
-   [X] Write `docker-compose.yml` defining Postgres, Redis, Celery, and Mailpit.
-   [X] Build `main.py` with basic health-check endpoint and verify container orchestration.

### Phase 2 --- Data Layers & Validation
-   [X] Establish database engine and baseline relational tables in `db/models.py`.
-   [X] Implement `schemas/chat.py` to match the exact JSON shape sent by the React frontend.
-   [X] Implement robust error handling for missing/malformed payloads.

### Phase 3 --- Core Endpoint Wiring
-   [X] Connect `routes_chat.py` to accept the widget submissions.
-   [X] Verify frontend-to-backend communication over local networks (handle CORS).
-   [X] Test real data persistence into the local Postgres instance.

### Phase 4 --- Workers & Free Notifications
-   [X] Hook up Celery to communicate natively with the Redis broker.
-   [X] Build `services/excel_gen.py` to query databases and generate Excel sheets dynamically.
-   [X] Build `services/email_sender.py` using standard `smtplib`.
-   [X] Test end-to-end email generation using local Mailpit dashboard.