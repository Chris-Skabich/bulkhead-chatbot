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

### Phase 5 — Admin Settings & Urgency Engine (Current Phase)
-   [ ] **Database Migration:** Migtate to MongoDB and expand PostgreSQL schema with a `ClientSettings` table to store email targets, business hours, and custom urgency thresholds.
-   [ ] **Create Admin Endpoints:** Build endpoints in `routes_admin.py` to allow business owners to configure and fetch their preferences.
-   [ ] **AI Timeline Normalizer:** Build an LLM utility in `services/nlp_parser.py` that translates messy human timeline entries (e.g., "75 days", "2 weeks") into standardized decimals (e.g., `2.5` months, `0.5` months) rounded to the nearest tenth.
-   [ ] **Urgency Ranking Logic:** Update the daily Excel report generator to cross-reference the normalized timeline against the client's custom urgency limit, sorting and highlighting priority jobs first.

### Phase 6 — Security, Anti-Abuse & Monetization (Pre-Launch)
-   [ ] **Rate Limiting:** Implement a Redis-based token bucket rate limiter on the public `/leads` endpoint to block automated spam.
-   [ ] **Input Sanitization:** Guard the entry pipeline against SQL injection and cross-site scripting (XSS) payload variants.
-   [ ] **SaaS License Kill Switch:** Implement API key checks. If a client cancels their subscription, their unique key is flagged as inactive, automatically hiding or disabling the chatbot on their website.
-   [ ] **AI Gateway Integration:** Standardize backend API calls to allow seamless hot-swaps between LLM providers (Gemini, OpenAI, Anthropic) to optimize speed and cost metrics.

---

## Database Schema Evolution

To support multi-tenancy and custom settings for each bulkhead company, the PostgreSQL database is expanded to support relational client and lead mappings.

### 1. `client_settings` Table
Stores business configurations, operating hours, and custom lead-prioritization thresholds.

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Unique identifier for the bulkhead business. |
| `api_key` | String (Unique) | Secure credential used by the widget to fetch settings and post leads. |
| `company_name` | String | Name of the business. |
| `report_email` | String | The target email address where morning Excel reports are dispatched. |
| `business_hours` | JSONB | Operating hours config (e.g., `{"timezone": "EST", "work_days": [1,2,3,4,5], "start": "08:00", "end": "17:00"}`). |
| `urgency_threshold` | Float | Maximum timeline in months (e.g., `1.0`) that classifies a lead as urgent. |
| `is_active` | Boolean | Licensing flag. Set to `False` to instantly disable the front-end widget. |

### 2. `leads` Table (Updated)
Maps captured homeowner information to specific clients, incorporating AI-normalized data.

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Unique identifier. |
| `client_id` | Integer (FK) | Maps the lead back to the specific business in `client_settings`. |
| `name` | String | Homeowner name. |
| `phone` | String | Homeowner phone number. |
| `email` | String | Secondary contact email. |
| `project_type` | String | Categorized project type (*Failing Structure*, *New Build*, *Maintenance*). |
| `linear_feet` | Integer | Estimated project size. |
| `timeline_raw` | String | Unfiltered timeline input from user (e.g., *"In about three weeks"*). |
| `timeline_months`| Float | **AI-Generated:** Standardized decimal value in months (e.g., `0.7`). |
| `created_at` | DateTime | Timestamp of lead submission. |

---

## Core System Services (Under the Hood)

### 1. AI Timeline Normalizer (`nlp_parser.py`)
To prevent inconsistent text formatting from breaking database sorting filters, our backend utilizes an AI parser to standardize schedule data.

```text
User Input: "I want this done in 3 weeks" 
                        │
                        ▼ (LLM Translation Prompt)
Result: { "standardized_months": 0.7 } ──► Saved to Postgres
```

By standardizing timelines into decimals (representing months), we run direct mathematical comparisons:

$$\text{Is Urgent} = (\text{timeline\_months} \le \text{client's urgency\_threshold})$$

### 2. Smart Excel Prioritizer (`excel_gen.py`)
When compiling the morning spreadsheet, the Excel generator checks the client's setting preferences. If sorted by urgency, the backend prioritizes critical leads using direct database queries:

```python
# Conceptual prioritization query
leads = db.query(Lead).filter(Lead.client_id == client_id).order_by(
    Lead.timeline_months.asc(),  # Shortest timeline first
    Lead.linear_feet.desc()      # Tie-breaker: Largest job first
).all()
```

---

## Security, Anti-Abuse & Hostinger Deployment

### 1. Anti-Spam Rate Limiting
Because the frontend widget is exposed to the public, the `/leads` route is protected by a **Token Bucket Rate Limiter** managed in Redis. 
- Limits individual IP addresses to a maximum of **3 lead submissions per hour** to prevent automated script attacks from lock up your database or exhausting SMTP limits.

### 2. Hostinger Embed Isolation
Because customer bulkhead websites are typically built using standard drag-and-drop web builders, the integration script is designed to load dynamically using standard custom HTML injection blocks:

```html
<!-- Hostinger Website Embed Template -->
<div id="bulkhead-bot-root"></div>
<script 
  src="[https://your-backend-domain.com/static/bulkhead-widget.js](https://your-backend-domain.com/static/bulkhead-widget.js)" 
  data-client-key="SECURE_CLIENT_API_KEY_HERE">
</script>
```

Upon initialization, the widget reads the custom `data-client-key` attribute and queries your FastAPI backend:
1. Verifies that the key is valid and subscription licensing is active (`is_active == True`).
2. Fetches the custom operating hours config.
3. If valid, the chat widget renders. If invalid or suspended, the script exits silently, leaving the host site completely clean.