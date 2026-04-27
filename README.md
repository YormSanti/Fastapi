# FastAPI Postgres App

FastAPI project structured with SQLAlchemy, Pydantic schemas, service functions, routes, and Alembic migrations.

## Setup

```powershell
.\env\Scripts\python.exe -m pip install -r requirements.txt
```

Update `.env` with your PostgreSQL username, password, host, port, and database name:

```env
DATABASE_URL=postgresql+psycopg2://postgres:123@localhost:5432/fastapiDB
```

## Run Migrations

```powershell
.\env\Scripts\alembic.exe upgrade head
```

## Run App

```powershell
.\env\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## User Endpoints

- `POST /api/users`
- `GET /api/users`
- `GET /api/users/{user_id}`
