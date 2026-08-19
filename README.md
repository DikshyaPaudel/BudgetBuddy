# BudgetBuddy 

BudgetBuddy is a Django web app for tracking personal income and expenses. Log transactions by category, view spending stats, and export your data to Excel — all behind a simple login/signup flow (including Google sign-in).

## Features

- 🔐 **Authentication** — email/password signup with verification, plus Google OAuth2 login
- 💸 **Expense tracking** — add, edit, delete, and categorize expenses (Health, Groceries, Fuel, etc.)
- 💵 **Income tracking** — log income by source
- 🔍 **Search** — filter transactions by amount, date, description, or category
- 📊 **Stats page** — visual breakdown of spending and income
- 📁 **Excel export** — download your expense data as an `.xlsx` file
- 📄 **Pagination** — browse transactions in manageable pages

## Tech Stack

- **Backend:** Django 5, Django REST Framework
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript (Django templates)
- **Auth:** `social-auth-app-django` (Google OAuth2), custom email verification
- **Other:** `openpyxl` / `xlwt` (Excel export), `Pillow`, `gunicorn`, `whitenoise`
- **Containerization:** Docker + Docker Compose

## Getting Started

### Option 1: Docker (recommended)

```bash
git clone https://github.com/DikshyaPaudel/BudgetBuddy.git
cd BudgetBuddy/trackexpenses
docker compose up --build
```

This spins up the Django app and a PostgreSQL database together, and runs migrations automatically on startup.

The app will be available at **http://localhost:8000**.

### Option 2: Local (Pipenv)

```bash
git clone https://github.com/DikshyaPaudel/BudgetBuddy.git
cd BudgetBuddy
pipenv install
pipenv shell
cd trackexpenses
python manage.py migrate
python manage.py runserver
```

You'll need a local PostgreSQL instance (or adjust the database settings for SQLite) and to set any required environment variables — see `trackexpenses/settings.py` for `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` / `SECRET` and email settings if you want Google login and email verification to work.
