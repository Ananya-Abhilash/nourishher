# NourishHer AI — Day 1

NourishHer AI is an evidence-focused nutrition and health information application. This Day 1 foundation provides account management, a private health profile, initial data models, and a React navigation shell. It does not provide medical advice.

## Architecture

- **Backend:** Django + Django REST Framework, token-authenticated JSON API.
- **Frontend:** React + Vite + React Router + Axios.
- **Data:** SQLite by default for local setup; PostgreSQL is selected automatically when `DATABASE_URL` is set.

## Folder structure

```
backend/     Django project and modular API apps
frontend/    Vite React client
```

Backend apps are `users`, `profiles`, `labs`, `nutrients`, `research`, `recommendations`, and `agents`. The latter three are intentional placeholders for later development.

## Setup

### Backend

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

On Linux/macOS activate with `source venv/bin/activate`. SQLite needs no further configuration. To use PostgreSQL, set `DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DBNAME` in `backend/.env` and migrate.

### Frontend

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```
tree /f /a > output2.txt
Open the address printed by Vite (normally `http://localhost:5173`). `VITE_API_URL` defaults to `http://127.0.0.1:8000/api` if omitted.

## Environment variables

`backend/.env`: `SECRET_KEY`, `DEBUG`, `DATABASE_URL`, `ALLOWED_HOSTS`; also optionally `CORS_ALLOWED_ORIGINS`.

`frontend/.env`: `VITE_API_URL`.

## API endpoints

| Endpoint | Methods | Purpose |
| --- | --- | --- |
| `/api/auth/register/` | POST | Create an account and return an auth token |
| `/api/auth/login/` | POST | Log in and return an auth token |
| `/api/auth/logout/` | POST | Revoke the current token |
| `/api/auth/me/` | GET | Get current user |
| `/api/profile/` | GET, PUT | Read/update the current user’s health profile |
| `/api/labs/reports/` | GET, POST | Initial lab-report API structure |
| `/api/nutrients/` | GET | Read nutrient records when they exist |

Authenticated requests use `Authorization: Token <token>`. The React client manages it centrally and clears it if the token becomes invalid.

## Current functionality

- Registration, login, logout, persisted frontend auth state, and protected routes.
- Private health profile creation and update.
- Landing page, dashboard, sidebar navigation, lab-entry skeleton, and clearly marked placeholder pages.
- Foundational `LabReport`, `LabResult`, and `Nutrient` models.

## Deliberately not implemented

AI agents, LLMs, RAG, web/research ingestion, vector databases, health interpretation, medical or supplement advice, blood-test extraction, deficiency detection, Celery, Redis, and complex analytics are intentionally deferred beyond Day 1.
