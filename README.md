
# 📧 Email Automation & Reminder System

A modular Python workflow automation system that reads contact lists and reminder schedules from CSV files, personalizes reusable email templates, schedules one-off or recurring alerts, sends emails securely via SMTP TLS (or simulates safely in Dry-Run mode), and generates audit logs and CSV delivery reports.

---

## 🎯 Problem Statement
Teams in Operations, HR, Sales, Finance, and Training spend hours manually sending repetitive reminders for meetings, invoices, onboarding tasks, and workshops. Manual emailing is error-prone, lacks centralized delivery tracking, and does not scale.

## 💼 Industry Relevance
- **HR & Admin:** Onboarding checklists, policy reminders, interview alerts
- **Finance & Operations:** Payment due notices, vendor follow-ups, SLA reminders
- **Sales & Training:** Demo follow-ups, cohort session links, renewal alerts

---

## ✨ Key Features
- **CSV-Driven Workflow:** Manage contacts (`contacts.csv`) and reminder rules (`reminders.csv`) without editing code.
- **Automated Eligibility Filtering:** Automatically skips inactive contacts or disabled reminders.
- **Dynamic Personalization:** Injects `{name}`, `{company}`, `{event_title}`, `{due_date}`, and `{amount}` into `.txt` templates.
- **Safe Dry-Run Simulation:** Test the entire pipeline locally without sending real emails.
- **Local Scheduler:** Supports immediate single execution (`--mode once`) and recurring scheduled cycles (`--mode schedule`).
- **Secure Credential Handling:** Loads SMTP credentials from environment variables via `.env`.
- **Audit Logging & Reporting:** Logs every event to `logs/automation.log` and exports timestamped reports to `outputs/`.

---

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Data Processing:** Pandas
- **Email & Transport:** `smtplib`, `email.message` (SMTP + STARTTLS)
- **Scheduling:** `schedule`, `datetime`
- **Configuration & Logging:** `python-dotenv`, `logging`, `argparse`

---

## 📂 Folder Structure
```text
Email-Automation-Reminder-System/
├── data/               # Sample contacts.csv & reminders.csv
├── templates/          # Email templates with dynamic placeholders
├── src/                # Modular Python source files
├── outputs/            # Generated CSV delivery reports
├── logs/               # Execution log files
├── images/             # Project screenshots
├── .env.example        # Environment variable template
├── .gitignore
├── main.py             # CLI entry point
└── requirements.txt

## Authors

* **GitHub:** [nandiniverma2009](https://github.com)
* **LinkedIn:** [NandiniVerma](https://linkedin.com)
