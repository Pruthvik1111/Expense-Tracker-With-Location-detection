<div align="center">

# 💸 expense.track

### A location-aware expense tracker — see *where* your money goes, not just where it went.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Leaflet](https://img.shields.io/badge/Leaflet.js-199900?style=flat-square&logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](#license)

</div>

---

## 📖 Overview

**expense.track** is a full-stack personal expense tracker built with **FastAPI**. Beyond the usual add/view/delete flow, every expense can be tagged with the **exact GPS coordinates** of where it happened — captured straight from the browser's Geolocation API — and plotted live on an interactive **Leaflet.js** map.

The result: instead of a flat list of numbers, you get a visual map of your spending — that ₹250 coffee pin sitting right next to the café you bought it at.

## ✨ Features

- 🔐 **User accounts** — sign up, log in, and log out with session-based auth (SHA-256 hashed passwords)
- ➕ **Add expenses** — title, category, and amount, with per-user isolation (you only ever see your own data)
- 📍 **One-click location tagging** — hit "Detect" and the browser's Geolocation API captures your lat/lng and drops it into the form automatically
- 🗺️ **Interactive expense map** — every located expense renders as a pin on an OpenStreetMap/Leaflet map, with a popup showing title, category, amount, and timestamp
- 🖱️ **Click-to-fly** — click any expense in the list and the map flies to its pin
- 💰 **Live running total** — a banner shows total spend and expense count, updated in real time
- 🕒 **Live clock** — a small touch of polish on the dashboard
- 🗑️ **Delete expenses** — remove entries you no longer need, scoped to the logged-in user
- 🎨 **Custom dark UI** — hand-built styling (no framework), designed around a dark surface + lime-green accent palette

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) (Python) |
| **ORM / Database** | [SQLAlchemy](https://www.sqlalchemy.org/) + MySQL |
| **Templating** | Jinja2 |
| **Sessions** | Starlette `SessionMiddleware` |
| **Frontend** | Vanilla HTML/CSS/JS |
| **Maps** | [Leaflet.js](https://leafletjs.com/) + OpenStreetMap tiles |
| **Geolocation** | Browser Geolocation API |

## 📂 Project Structure

```
Expense-Tracker-With-Location-detection/
├── main.py              # FastAPI app: models, routes, auth, session logic
├── database.py          # Database session/engine helpers
├── models.py             # SQLAlchemy models
├── templates/
│   ├── login.html         # Login page
│   ├── signup.html        # Signup page
│   └── dashboard.html     # Main dashboard: form, expense list, Leaflet map
├── requirements.txt      # Python dependencies
└── .gitignore
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A running MySQL server
- `pip`

### 1. Clone the repository

```bash
git clone https://github.com/Pruthvik1111/Expense-Tracker-With-Location-detection.git
cd Expense-Tracker-With-Location-detection
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy mysql-connector-python jinja2 python-multipart itsdangerous
```

> 💡 `requirements.txt` is currently empty — run `pip freeze > requirements.txt` after installing so future setup is a one-liner (`pip install -r requirements.txt`).

### 4. Configure your database

Create a MySQL database:

```sql
CREATE DATABASE expense_tracker;
```

Then set your connection string as an **environment variable** rather than hardcoding it (see [Security Notes](#-security-notes) below):

```bash
# .env (do not commit this file — add it to .gitignore)
DATABASE_URL=mysql+mysqlconnector://<user>:<password>@localhost/expense_tracker
SECRET_KEY=<a-long-random-string>
```

And load it in `main.py`, e.g. with `python-dotenv`:

```python
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
```

Tables are created automatically on first run via `Base.metadata.create_all(bind=engine)` — no manual migration needed.

### 5. Run the app

```bash
uvicorn main:app --reload
```

Visit **http://127.0.0.1:8000** — you'll be redirected to `/login`. Sign up for an account to get started.

## 🖱️ Usage

1. **Sign up / log in** to your account.
2. On the dashboard, fill in a **title**, **category**, and **amount**.
3. Click **📍 Detect** to grab your current location (your browser will ask for permission) — or leave it blank if you'd rather not tag a location.
4. Hit **Add Expense** — it appears in your list and, if located, as a pin on the map.
5. Click any expense card to **fly to its pin** on the map.
6. Click **Delete** to remove an expense.

## 🗺️ Roadmap

- [ ] Populate `requirements.txt` with pinned dependency versions
- [ ] Move secrets (DB credentials, session key) into environment variables
- [ ] Category-wise spending breakdown / charts
- [ ] Date-range filtering and search
- [ ] Edit expenses (currently add/delete only)
- [ ] Export expenses to CSV
- [ ] Password hashing upgrade (bcrypt/argon2 instead of raw SHA-256)
- [ ] Deploy a live demo

## 🔒 Security Notes

A few things worth tightening before this goes anywhere near production or a public deployment:

- **Hardcoded secrets**: the database connection string and session `secret_key` currently live directly in `main.py`. Since this repo is public, those values are already exposed — rotate the MySQL password and generate a new session secret, then load both from environment variables going forward.
- **Password hashing**: passwords are hashed with plain SHA-256. For real-world use, switch to a purpose-built algorithm like `bcrypt` or `argon2` (e.g. via `passlib`), which are designed to resist brute-forcing.
- **`.env` in `.gitignore`**: once you move secrets to a `.env` file, make sure it's excluded from version control.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/Pruthvik1111/Expense-Tracker-With-Location-detection/issues) or open a PR.

## 📄 License

This project is available under the [MIT License](LICENSE).

## 👤 Author

**Pruthvik**
🎓 B.E. in AI & ML, Sri Krishna Institute of Technology (SKIT), Bengaluru
🔗 [GitHub](https://github.com/Pruthvik1111)

---

<div align="center">
Made with ☕ and a little too much geolocation debugging.
</div>