# Bulkhead After-Hours Lead Bot Frontend

A lightweight, embeddable React chatbot widget designed for marine construction companies. The widget compiles into a single JavaScript file (`bulkhead-widget.js`), making it easy to embed into any website using a simple `<script>` tag.

---

## Features

- React 18 powered chatbot interface
- Single-file deployment (`bulkhead-widget.js`)
- Embeddable on any website
- Scoped CSS to prevent style conflicts
- Rule-based conversation flow
- Lead capture and backend integration
- Linear-foot measurement parsing and normalization

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| React 18 | UI Framework |
| Vite | Bundler & Build Tool |
| CSS | Styling |
| vite-plugin-css-injected-by-js | Inject CSS into JS bundle |
| Custom React Hooks | State Management |

---

## Project Structure

```text
bulkhead-widget-frontend/
├── public/
│   └── index.html
│
├── src/
│   ├── assets/
│   │   └── Static assets
│   │
│   ├── components/
│   │   ├── ChatWindow.jsx
│   │   ├── MessageList.jsx
│   │   ├── MessageBubble.jsx
│   │   └── InputArea.jsx
│   │
│   ├── hooks/
│   │   └── useChatFlow.js
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── utils/
│   │   └── unitConverter.js
│   │
│   ├── index.css
│   └── main.jsx
│
├── package.json
├── vite.config.js
└── README.md
```

---

## Architecture Overview

The widget is designed to behave as a self-contained application that can be embedded into an existing website.

### Application Flow

```text
Host Website
     │
     ▼
main.jsx
     │
     ▼
ChatWindow
     │
     ├── MessageList
     ├── MessageBubble
     └── InputArea
     │
     ▼
useChatFlow
     │
     ▼
api.js
     │
     ▼
FastAPI Backend
```

---

## Component Responsibilities

### `main.jsx`

Entry point for the widget.

Responsibilities:

- Locate the host page root element
- Mount the React application
- Initialize the chatbot

Example:

```html
<div id="bulkhead-bot-root"></div>
```

### `ChatWindow.jsx`

Primary chatbot container.

Responsibilities:

- Floating action button
- Open/close chat window
- Widget layout and shell

### `MessageList.jsx`

Conversation display area.

Responsibilities:

- Render conversation history
- Auto-scroll to newest messages

### `MessageBubble.jsx`

Individual message styling.

Responsibilities:

- Differentiate bot vs. user messages
- Handle timestamps (optional)

### `InputArea.jsx`

User interaction controls.

Responsibilities:

- Text input
- Send button
- Quick reply options

### `useChatFlow.js`

Conversation state machine.

Example flow:

```text
Greeting
   ↓
Name
   ↓
Phone Number
   ↓
Project Type
   ↓
Linear Feet
   ↓
Timeline
   ↓
Lead Submission
```

### `unitConverter.js`

Utility for normalizing project measurements.

Examples:

```text
"100 feet" → 100
"100 ft"   → 100
"100'"     → 100
```

Returns a standardized integer value for backend storage.

### `api.js`

Backend communication layer.

Responsibilities:

- Submit completed leads
- Handle API responses
- Surface submission errors

Example payload:

```json
{
  "name": "Chris Skabich",
  "phone": "123-456-7890",
  "project_type": "Bulkhead Repair",
  "linear_feet": 150,
  "timeline": "Within 3 months"
}
```

---

## Local Development

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

Ensure your local test page contains:

```html
<div id="bulkhead-bot-root"></div>
```

---

## Production Build

Generate the deployable widget:

```bash
npm run build
```

Output:

```text
dist/
└── bulkhead-widget.js
```

The final build contains:

- React application
- CSS styles
- Widget logic

All bundled into a single JavaScript file.

---

## Client Installation

Clients can embed the chatbot by adding the following snippet before the closing `</body>` tag:

```html
<div id="bulkhead-bot-root"></div>

<script src="https://your-hosting-domain.com/bulkhead-widget.js"></script>
```

Once loaded, the widget automatically mounts itself into the provided container.

---

## Development Roadmap

### Phase 1 — Core Widget

- [ ] Build `main.jsx`
- [ ] Create scoped widget styles
- [ ] Build floating chat launcher
- [ ] Implement expandable chat window

### Phase 2 — Messaging UI

- [ ] Build `MessageList.jsx`
- [ ] Build `MessageBubble.jsx`
- [ ] Build `InputArea.jsx`
- [ ] Add auto-scroll behavior

### Phase 3 — Conversation Engine

- [ ] Implement `useChatFlow.js`
- [ ] Build question sequencing
- [ ] Add validation logic
- [ ] Add quick reply support

### Phase 4 — Data Processing

- [ ] Build `unitConverter.js`
- [ ] Normalize linear-foot values
- [ ] Validate collected lead data

### Phase 5 — Backend Integration

- [ ] Connect to FastAPI backend
- [ ] Submit completed leads
- [ ] Handle API errors
- [ ] Add submission confirmation state