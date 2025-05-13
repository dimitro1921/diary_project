# 🧠 Personal Knowledge & Reflection Diary Bot (MVP)

A modular, scalable MVP of a Telegram bot and REST API for capturing personal thoughts, ideas, and daily reflections — designed to evolve into a full web and Android application.

---

## 📌 Project Objective

Create a system that allows users to:
- Save ideas, thoughts, knowledge, or self-reflection entries at any time.
- Receive a daily reflection prompt via Telegram.
- Store all entries with structured metadata.
- Retrieve or export their personal archive.
- Ensure privacy: users only see their own data.

---

## Project Structure

```
diary_project/
├── app/                          # Shared logic (models, DB, logic)
│   ├── __init__.py
│   ├── config.py                 # Load .env variables
│   ├── db.py                     # DB engine and session
│   ├── models.py                 # SQLAlchemy models
│   ├── schemas.py                # Pydantic schemas
│   ├── crud.py                   # CRUD operations
│   └── exporter.py               # Export to Markdown
│
├── api/                          # FastAPI app
│   ├── __init__.py
│   ├── main.py                   # Start API + scheduler
│   ├── routes.py                 # API endpoints
│   ├── auth.py                   # Optional auth
│   ├── scheduler.py              # Prompt scheduler
│   └── send_prompt.py            # Send Telegram prompts
│
├── bot/                          # Telegram bot (API client)
│   ├── __init__.py
│   ├── main.py                   # Bot entry point
│   ├── handlers.py               # Bot commands
│   ├── states.py                 # FSM states
│   └── client.py                 # Call API
│
├── prompts/                      # Reflection questions
│   └── reflection_questions.txt
│
├── data/                         # SQLite database
│   └── diary.db
│
├── .env                          # Config vars
├── requirements.txt              # Dependencies
├── Dockerfile                    # Docker image
├── docker-compose.yml            # API + bot setup
└── README.md
```
---

## ⚙️ Tech Stack

- **Python 3.11+**
- **Aiogram 3.7.0** — Telegram bot framework
- **FastAPI** — REST API backend
- **SQLite** — Local database for MVP
- **SQLAlchemy** — ORM for all DB logic
- **Pydantic** — Validation schemas
- **APScheduler** — For daily prompt scheduling
- **Docker** & **Docker Compose**

---

## 🔁 Data Model Example

```json
{
  "user_id": 12345678,
  "message_id": 217,
  "username": "john_doe",
  "timestamp": "2025-05-07T14:43:21",
  "text": "Learned about SQLite transactions.",
  "entry_type": "idea",
  "tags": "#sqlite,#python",
  "source": "manual",
  "date_only": "2025-05-07"
}
```

---

## 📜 Core Features

- **Message Logging**: Each user message is saved with detailed metadata, including entry type, tags, timestamp, and source.

- **Reflection Prompt**: The bot sends a daily reflection question at 21:00 (Kyiv time). The user’s reply is stored automatically as a `reflection` entry.

- **Privacy First**: All entries are stored per user and are never visible to anyone else. Telegram `user_id` is used as the unique identifier.

- **Export to Markdown**: Users can export their personal archive using the `/export` command or a corresponding API endpoint. Markdown is the default format.

- **Stateful Command Guidance**: The `/idea` and `/reflect` commands set a short-lived state to treat the *next* message as an idea or reflection.  
  The bot replies with a short explanation like:  
  `"✅ Got it. Your next message will be saved as an idea."`  
  If no message is sent within 60 seconds, or another command is issued, the state is cleared.


---

## 🧠 Future Features

- Tag filtering and search
- Web interface
- Android mobile application
- Multi-language prompt support
- OAuth2 / Google Auth
- Data sync across devices

---

## 🚀 Setup & Run Locally

🚧 *Coming soon...*

---

## 🐳 Docker Usage

🚧 *Coming soon...*

---

## 🧪 API Reference

🚧 *Coming soon...*

---

## 🔐 Security Notes

- Telegram user ID is used as a unique user key.
- All data is stored locally in SQLite during MVP stage.
- No third-party integrations or cloud sync are used (yet).

---

## 🧭 License

MIT — free to use, modify, and build upon.

---

## 🙋 Author

Built with 💬, 🧠 and ☕ by [Your Name].
