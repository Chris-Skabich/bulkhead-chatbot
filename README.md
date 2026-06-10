# Bulkhead & Marine Construction After-Hours Lead Bot

## Overview

The **Bulkhead After-Hours Lead Bot** is a specialized, automated intake system designed specifically for marine construction and shoreline protection companies. Deployed on your website, this chatbot acts as a 24/7 digital sales assistant. It activates automatically outside of your configured business hours to capture, qualify, and organize incoming leads so your team can hit the ground running the next morning.

By asking targeted, industry-specific questions—from linear footage to site accessibility—the bot ensures that casual inquiries are separated from urgent, high-value projects before your sales team spends a minute on them.

---

## Core Features

* **Customizable Operating Hours:** Automatically toggles on/off based on your specific business hours.
* **Intelligent Unit Conversion:** Allows users to input project dimensions in various formats and automatically converts them to standardized **linear feet** for your records.
* **Automated Excel Export:** Compiles all captured data into a neatly formatted Excel spreadsheet (one row per job/lead).
* **Scheduled Daily Delivery:** Emails the compiled lead sheet to your team at a designated time each morning.
* **Custom Lead Sorting:** Allows admins to prioritize how leads are presented (e.g., sort chronologically by time received, or sort by job size/urgency).

---

## The Chatbot Flow (User Experience)

When a visitor lands on your site after hours, the chatbot initiates the following sequence:

### 1. The Welcome & Contact Capture
* **Greeting:** Politely alerts the visitor that the office is currently closed, but a team member will reach out the next business day.
* **Primary Contact Info:** Collects Name and Phone Number.
* **Callback Preference:** Asks for the *best time to call* during the next business day.
* **Backup Contact:** Requests an Email Address in case they cannot be reached by phone.

### 2. Project Scope & Assessment
* **Project Type:** Determines the nature of the work (e.g., new bulkhead installation, repair/replacement of a failing structure, seawall, dock-related, or typical maintenance/erosion control).
* **Current Issue:** Asks what prompted the inquiry (e.g., visible erosion, leaning wall, flooding, recent storm damage) and how long it has been an issue to gauge urgency.
* **Project Size:** Captures the approximate size of the area needing work. *The bot will automatically convert the user's dimension inputs into total linear feet.*
* **Existing Conditions:** Asks about the current structure (if applicable), including age and material (wood, vinyl, steel sheet pile, concrete).

### 3. Qualification & Logistics
* **Location:** Requests the property address to confirm waterfront access, permit jurisdiction, and service area viability.
* **Authority:** Confirms if the user is the primary decision-maker (Property Owner, HOA Representative, Business Manager, etc.).
* **Documentation:** Inquires if they already have engineering reports, active permits, or previous quotes.
* **Timeline:** Determines when they want the project completed (e.g., emergency post-storm, within the next month, or planning for next year).

### 4. Open-Ended Details & Sign-Off
* **Additional Context:** Prompts the user to provide any other details, specific material preferences, environmental concerns, or site accessibility issues (e.g., boat access needs).
* **Closing Expectation:** Reassures the user that their information has been securely captured and confirms that a specialist will contact them at their preferred time.

## Lead Qualification Criteria (Behind the Scenes)

This chatbot is designed around a marine-tailored BANT (Budget, Authority, Need, Timeline) framework. The data collected allows your team to score and filter leads immediately based on:

| Qualification Metric | Why It Matters for Bulkhead Companies |
| :--- | :--- |
| **Need / Urgency** | Differentiates between a casual inquiry and an active emergency. Knowing if a wall is actively failing versus wanting an aesthetic upgrade helps prioritize callbacks. |
| **Scope & Feasibility** | 50 ft. vs. 300 ft. drastically changes the project scale. Address collection flags potential regulatory hurdles (Army Corps, state agencies) early on. |
| **Authority** | Establishes who holds the purse strings. Avoids wasting time negotiating with middlemen who cannot authorize the build. |
| **Timeline** | Aligns the customer's expectations with your current availability and the reality of the permitting process (which can take months). |
| **Budget Indicators** | While direct budget questions can be included, the combination of linear footage, material requests, and existing damage gives your estimators a clear picture of the financial scope (tens to hundreds of thousands of dollars) before the first call. |

---

## Admin Dashboard & Data Export

### Lead Sheet Generation
All completed conversations are parsed and exported into a master Excel document.
* **Format:** One horizontal row equals one complete job profile.
* **Delivery:** Sent via email automatically at the start of your workday (e.g., 7:00 AM).

### Custom Display Preferences
Admins can customize how the daily lead sheet is organized so the most important information is seen first:
* **Sort by Time:** Chronological list of when the leads came in.
* **Sort by Job Size:** Prioritizes leads based on the highest linear footage.
* **Sort by Urgency:** Flags emergency repairs or failing structures to the top of the list.
