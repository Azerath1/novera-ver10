# MyNovelProject

## Backend (FastAPI)

1. cd backend
2. python -m venv venv
3. source venv/bin/activate (or venv\Scripts\activate on Windows)
4. pip install -r requirements.txt
5. Create .env with DATABASE_URL=postgresql://user:pass@localhost/db
6. uvicorn src.main:app --reload

## Frontend (Next.js)

1. cd frontend
2. npm install
3. npm run dev

API: http://localhost:8000
Frontend: http://localhost:3000
