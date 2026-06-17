AI Agent & Chatbot Backend Services

Welcome to the backend repository for our AI Agent and Chatbot platform. This document serves as the central engineering guide for understanding the system architecture, component responsibilities, and local development workflows.

Our backend is designed to handle high-concurrency, asynchronous chat sessions, reliable background task scheduling, and secure data persistence.
Features

    Asynchronous Chat Session Management: Event-driven architecture to handle concurrent, real-time client-agent interactions without blocking the main event loop.

    Robust Task Scheduling: Distributed message queues to manage long-running background jobs, retries, and scheduled tasks.

    Automated Reporting Pipeline: Scheduled worker systems that compile system/lead metrics into Excel reports and distribute them daily.

    Secure Data Multi-Tenancy: Isolated storage of client configurations, agent prompts, and sensitive lead data.

Tech Stack

The core architecture relies on a decoupled, production-grade JavaScript/TypeScript ecosystem:

    Application Framework: Node.js with NestJS (preferred for its native dependency injection and modular architecture) or Express (configured with TypeScript).

    Database & ORM: PostgreSQL hosted via Supabase, utilizing Prisma ORM for type-safe schema management and migrations.

    Task Scheduling & Queues: Redis coupled with BullMQ to handle heavy background processing and cron schedules.

    Email Infrastructure: Resend (or SendGrid) API for transactional emails and daily Excel report delivery.

Project Structure & Architecture Overview

Our backend adheres to a modular, decoupled architecture to ensure that heavy background operations (like report generation) never degrade the performance of real-time chat sessions.
Repository Layout
Plaintext

### Repository Layout

```text
backend/
├── src/
│   ├── app.module.ts          # Main application bundle
│   ├── modules/
│   │   ├── chat/              # Chat sessions, WebSocket/SSE gateways
│   │   ├── config/            # Client & Agent configurations
│   │   ├── leads/             # Lead generation and tracking data
│   │   ├── queue/             # BullMQ processors and workers
│   │   └── reporting/         # Excel generation and Email service hooks
│   └── common/                # Guards, interceptors, and Prisma client
├── prisma/
│   └── schema.prisma          # Database schema definitions
├── dist/                      # Compiled production build
└── package.json
'''
High-Level Architecture Flow

    API Layer: Handles client configuration changes and active chatbot messaging traffic.

    Cache/Queue Layer: Offloads heavy, time-sensitive, or scheduled tasks (e.g., generating daily reports) away from the HTTP thread.

    Worker Layer: Consumes queue messages, queries PostgreSQL for lead data, compiles reports, and triggers the email API.

Component Responsibilities
1. API Layer (Node.js / NestJS)

    Session Management: Coordinates stateful or stateless chat sessions across multiple clients.

    Client Configurations: Exposes REST endpoints to update system prompts, agent personalities, and API keys.

    Ingestion: Captures lead information mid-conversation and securely pushes it to the database.

2. Persistence Layer (PostgreSQL & Prisma)

    Relational Integrity: Maps complex relations between Clients, Agents, Chat Sessions, and captured Leads.

    Data Security: Utilizes strict database constraints and row-level security (RLS) where applicable to prevent cross-tenant data leaks.

3. Task Scheduling (Redis + BullMQ)

    Asynchronous Offloading: Prevents API degradation by shifting report compilation to separate worker threads.

    Cron Management: Triggers a daily repeatable job at a designated time (e.g., 0 0 * * *) to compile metrics.

    Resiliency: Handles automatic retries with exponential backoff if the email service or database experiences transient downtime.

4. Reporting & Email Service (Resend / SendGrid)

    Data Compilation: Aggregates the previous 24 hours of lead data into structured Excel sheets.

    Delivery: Interfaces with Resend to reliably deliver multi-part MIME emails containing the file attachments to clients.

Local Development
Prerequisites

    Node.js (v18+ recommended)

    Docker (for running local PostgreSQL and Redis instances)

Step-by-Step Setup

    Clone and Navigate to Backend Folder:
    Bash

    cd backend

    Install Dependencies:
    Bash

    npm install



    Spin up Infrastructure (Docker Compose):
    Bash

    docker compose up -d

    (Ensure your docker-compose.yml includes services for postgres and redis).

    Run Database Migrations:
    Bash

    npx prisma migrate dev --name init

    Start the Development Server:
    Bash

    npm run start:dev

Production Build

To compile the TypeScript code into optimized, production-ready JavaScript:
Bash

# 1. Build the application
npm run build

# 2. Run prisma migrations against your production database
npx prisma migrate deploy

# 3. Start the production server
npm run start:prod

Deployment Node

    Ensure the environment variables point to your managed Supabase instance and production Redis cluster.

    If deploying to serverless environments (like Vercel), background workers should be decoupled into standard long-running cloud instances (like AWS ECS or DigitalOcean App Platform) since BullMQ requires a persistent event loop connection to Redis.

Development Roadmap

    [ ] Phase 1: Core API setup with NestJS/Express and Prisma schema definitions for Leads and Configurations.

    [ ] Phase 2: Integration of real-time chat framework (WebSockets or Server-Sent Events) and LLM orchestration pipeline.

    [ ] Phase 3: Redis and BullMQ infrastructure setup for handling basic background event tasks.

    [ ] Phase 4: Implementation of the Excel parsing/generation module and Resend email integration.

    [ ] Phase 5: Cron job scheduling implementation for automated daily reports and end-to-end testing.