# 📊 Automated Google Slides Deck Updater

Welcome to your Google Slides automation project! 

This project allows you to **automatically update a Google Slides presentation on-demand or whenever an event occurs**, without having to edit slides manually in your browser.

---

## 🧭 How It Works (Plain English Translation)

You don't need to know Python to use or modify this project! Here is how the pieces fit together:

```
┌─────────────────────────┐      ┌──────────────────────────┐      ┌─────────────────────────────┐
│  1. Your Data / Event   │ ───► │  2. config.json          │ ───► │  3. Python Script           │
│  (Metrics, Status, Date)│      │  (Easy Text Settings)    │      │  (translates & pushes updates)│
└─────────────────────────┘      └──────────────────────────┘      └──────────────┬──────────────┘
                                                                                  │
                                                                                  ▼
                                                                   ┌─────────────────────────────┐
                                                                   │  4. Live Google Slides Deck │
                                                                   │  (Updated automatically!)   │
                                                                   └─────────────────────────────┘
```

1. **`config.json`**: This is your control panel. You type your presentation ID and the text/numbers you want to show on your slides here.
2. **`run_update.sh`**: The launcher button. Whenever you want to push updates to your slide deck, you just run this command.
3. **`update_slides.py`**: The underlying engine written in Python. It reads `config.json`, talks to Google's server using the official Google Slides API, and updates your deck in seconds.

---

## 📁 Project Structure

| File / Folder | What it is for | Do you need to touch it? |
| :--- | :--- | :--- |
| 📄 `config.json` | Holds your Presentation ID and slide text replacements | **Yes** — update your data here or generate this file automatically |
| 📄 `run_update.sh` | Simple one-line launcher command | **Yes** — run this whenever you want to trigger an update |
| 🐍 `update_slides.py` | Python code that speaks to Google Slides API | **No** (unless you want new advanced features) — fully commented in English |
| 📄 `requirements.txt` | List of software packages needed | Run setup once |

---

## 🚀 Step-by-Step Setup Guide

### Step 1: Install Python Dependencies (One Time Only)
Open your terminal and run:
```bash
cd "/usr/local/google/home/jasminesummers/Documents/Insights Wizard"
pip install -r requirements.txt
```

### Step 2: Prepare your Google Slides Presentation
1. Open your Google Slides presentation in your browser.
2. Look at the URL in your browser address bar:
   `https://docs.google.com/presentation/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ12345/edit`
3. Copy the ID string between `/d/` and `/edit` (in the example above: `1aBcDeFgHiJkLmNoPqRsTuVwXyZ12345`).
4. Paste that ID into `config.json` under `"presentation_id"`.

### Step 3: Add Placeholders to your Google Slides
In your Google Slides text boxes, put placeholder tags anywhere you want automatic data filled in:
* `{{PROJECT_NAME}}`
* `{{LAST_UPDATED}}`
* `{{STATUS_SUMMARY}}`
* `{{METRIC_KEY_PERFORMANCE}}`
* `{{METRIC_TOTAL_USERS}}`

### Step 4: Run an Update On-Demand
Whenever an event occurs or you want to update your deck, run:
```bash
./run_update.sh
```

---

## 💡 How to Customize Without Writing Code

Open `config.json` in any text editor. It looks like this:

```json
{
  "presentation_id": "YOUR_GOOGLE_SLIDE_DECK_ID_HERE",
  "placeholders": {
    "{{PROJECT_NAME}}": "Q3 Engineering Automation",
    "{{STATUS_SUMMARY}}": "All systems healthy. Automated pipelines operating at 99.9% uptime.",
    "{{METRIC_KEY_PERFORMANCE}}": "+24.5%",
    "{{METRIC_TOTAL_USERS}}": "14,250"
  }
}
```

Simply edit the words on the right side of each line! The Python script will automatically scan every slide in your deck and replace `{{PROJECT_NAME}}` with `"Q3 Engineering Automation"`, and so on.
