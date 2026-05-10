# Frontend - AI Powered Online Reputation Management System

React + TypeScript + Vite frontend for the reputation dashboard.

## What this frontend does

- Collects business name/location input
- Calls backend API endpoints:
  - `POST http://localhost:8000/api/search`
  - `POST http://localhost:8000/api/respond`
- Displays review metrics, sentiment split, recommendations, and generated response text

## Prerequisites

- Node.js 18+
- Backend FastAPI server running on port `8000`

## Install

```bash
npm install
```

## Run

```bash
npm run dev
```

Open the Vite URL shown in terminal (usually `http://localhost:5173`).

## Backend dependency

This frontend expects the backend to be running from the project `backend` folder:

```bash
cd ../backend
python main.py
```

Backend docs should be available at `http://127.0.0.1:8000/docs`.

## Notes

- API URLs are currently hardcoded in `src/App.tsx` to `http://localhost:8000`.
- If you change backend port/host, update those URLs accordingly.
