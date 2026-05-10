# AI Powered Online Reputation Management System

A full-stack prototype for monitoring online reputation of restaurants/hotels.

- Search a business by name and location
- Pull web snippets from DuckDuckGo
- Use AI to generate structured review insights
- View dashboard metrics (rating, total reviews, sentiment split)
- Generate response suggestions for reviews

## Tech Stack

- Frontend: React + TypeScript + Vite (`frontend`)
- Backend: Python + FastAPI (`backend`)
- AI: Groq Chat Completions API
- Web data source: `ddgs` (DuckDuckGo search snippets)

## Project Structure

- `backend/main.py` - FastAPI app and API routes
- `backend/services/duckduckgo.py` - DuckDuckGo snippet fetcher
- `backend/services/ai_engine.py` - AI processing + summary generation
- `backend/requirements.txt` - Python dependencies
- `frontend/src/App.tsx` - main dashboard UI

## Prerequisites

- Python 3.10+
- Node.js 18+

## Setup

### 1) Backend setup

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Create `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 2) Frontend setup

```bash
cd frontend
npm install
```

## Run the app

Use two terminals.

### Terminal 1: Start backend

```bash
cd backend
# if using venv, activate first
python main.py
```

Backend API will be available at:

- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

### Terminal 2: Start frontend

```bash
cd frontend
npm run dev
```

Open the Vite URL shown in terminal (usually `http://localhost:5173`).

## Notes

- `totalReviews`, `averageRating`, and review entries are currently AI-generated from live search snippets, so values can vary across runs.
- This is suitable for prototype/demo workflows; you can later swap in a real provider API (Google Places/Yelp/Apify) for stable production metrics.
