# Bulkhead Chatbot - Frontend Widget

## Overview
This repository contains the frontend code for the **Bulkhead After-Hours Lead Bot**. It is built as a lightweight, embeddable React application. Rather than behaving like a traditional single-page application (SPA), this project is configured to compile entirely into a **single JavaScript file** (`bulkhead-widget.js`). This allows marine construction companies to easily add the chatbot to their existing websites using a simple `<script>` tag.

---

## Tech Stack
* **Framework:** React 18
* **Bundler:** Vite
* **Styling:** Standard CSS (Injected directly into the JS bundle via `vite-plugin-css-injected-by-js`)
* **State Management:** Custom React Hooks (`useChatFlow.js`)

---

## Folder Structure

bulkhead-widget-frontend/
├── public/
│   └── index.html             # Used ONLY for local testing/development
├── src/
│   ├── assets/                # Static assets (bot icons, company logos, SVGs)
│   ├── components/            # UI pieces
│   │   ├── ChatWindow.jsx     # The main pop-up container
│   │   ├── MessageList.jsx    # Scrollable area rendering the conversation
│   │   ├── MessageBubble.jsx  # Individual styling for user vs. bot messages
│   │   └── InputArea.jsx      # Text input and send button
│   ├── hooks/
│   │   └── useChatFlow.js     # State machine: Controls which question is asked next
│   ├── services/
│   │   └── api.js             # Handles POST requests sending lead data to the FastAPI backend
│   ├── utils/
│   │   └── unitConverter.js   # Parses user dimensions into standardized linear feet
│   ├── index.css              # Widget styles (scoped to avoid clashing with host site)
│   └── main.jsx               # Entry point: Mounts the React app to a specific DOM element
├── package.json               # Dependencies and scripts
├── vite.config.js             # Custom build settings for single-file output
└── README.md

## Getting Started (Local Development)

To run the chatbot locally in a simulated environment:
Bashnpm install
Bashnpm run dev
Open http://localhost:5173 in your browser. Note: You will need to ensure public/index.html has a div with the matching ID that main.jsx targets (e.g., <div id="bulkhead-bot-root"></div>).

## Building for Production
When the code is ready to be deployed or handed to a client, run:
Bash
npm run build
This will generate a dist folder containing a single file: bulkhead-widget.js.

## How Clients Embed the Widget
To install the bot, the client simply pastes the following snippet right before the closing </body> tag of their website:
HTML
<div id="bulkhead-bot-root"></div>
<script src="[https://your-hosting-domain.com/bulkhead-widget.js](https://your-hosting-domain.com/bulkhead-widget.js)"></script>



## Development Roadmap (Task List)
The following tasks outline the build process from the "outside in":
1. The Entry Point
main.jsx: Write the logic to find the host website's root div (e.g., #bulkhead-bot-root) and render the React tree inside it.
index.css: Add foundational, scoped CSS (using a distinct prefix like .bh-bot-container) so our styles don't break the client's website.

2. The User Interface (Components)
ChatWindow.jsx: Build the collapsible chatbot shell (a floating action button that opens the chat window).
MessageList.jsx: Create the auto-scrolling view that holds the conversation history.
MessageBubble.jsx: Design distinct visual styles for the Bot's prompts versus the User's replies.
InputArea.jsx: Build the text input field, send button, and optional "quick reply" buttons for common answers.

3. The Brains (State & Logic)
useChatFlow.js: Build the rule-based state machine. Map out the conversation sequence (Greeting -> Name -> Phone -> Project Type -> Linear Ft -> Timeline).
unitConverter.js: Create a regex/parsing utility that strips out words like "feet" or symbols like ' to ensure project size is always saved as a clean integer.

4. Backend Integration
api.js: Write the fetch/axios calls that trigger when the conversation finishes, sending the compiled JSON lead object to the Python FastAPI backend.