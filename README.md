# AI-Powered Online Reputation Management System

A minimal reputation dashboard for restaurants and hotels. The app aggregates review and mention data, classifies sentiment, summarizes customer feedback, and generates suggested response text.

## Tech stack

- **Frontend:** Next.js 14 + React + TypeScript
- **Backend:** Next.js API routes
- **AI integration:** GROQ API (optional, fallback templates used when no API key is configured)
- **Data sources:** Mock connectors / seeded review samples

## Architecture overview

1. **Business Search / Input**
   - User enters `businessName`, `location`, and an optional `website`.
   - The frontend posts this data to `/api/search`.

2. **Review Aggregation**
   - `app/api/search/route.ts` calls `lib/analysis.ts`.
   - `lib/analysis.ts` uses `lib/mockData.ts` as a seeded dataset representing multiple sources:
     - Google Reviews
     - Zomato
     - TripAdvisor
     - Reddit
     - X
     - Instagram Mention
   - The mocked connector is modular and can be extended with new source adapters later.

3. **AI Sentiment Analysis**
   - Reviews are classified using a lightweight rule-based analyzer in `lib/analysis.ts`.
   - Each review receives:
     - sentiment: Positive / Neutral / Negative
     - topic: food, service, ambience, pricing, hygiene, etc.
     - emotion: happy, frustrated, disappointed, impressed
     - priority: low / medium / high

4. **Dashboard UI**
   - The homepage renders overall metrics, sentiment split, top complaints/compliments, and recommendations.
   - Recent reviews are shown with summary metadata.
   - Each review includes a button to generate an AI-suggested response.

5. **AI Suggested Responses**
   - `app/api/respond/route.ts` calls `lib/ai.ts`.
   - If `GROQ_API_KEY` is configured, the GROQ API is used to generate a polite, empathetic reply.
   - Otherwise, the app returns a fallback template response.

## What is mocked vs completed

### Completed

- Business search UI
- Aggregated dashboard with:
  - total review count
  - average rating
  - sentiment split
  - review source breakdown
  - top complaints and compliments
  - recommended actions
- Review metadata extraction
- Suggested response generation (GROQ-enabled or fallback)
- Clean project structure for future real connector integration

### Mocked

- Review ingestion is seeded from `lib/mockData.ts`.
- No live scraping or external review platform integration.
- The AI sentiment extraction is rule-based rather than a full NLP pipeline.

## Future improvements

- Add real data connectors for Google, TripAdvisor, Zomato, Instagram, X/Twitter, and blogs.
- Replace rule-based sentiment/topic classification with an LLM or specialized sentiment API.
- Add database storage for review history, business profiles, and user accounts.
- Build an admin dashboard with filtering, historical trends, and response templates.
- Add charts for trend analysis, sentiment over time, and source volume.
- Implement a secure webhook or scheduling job to refresh review data periodically.

## Setup and run

1. Install dependencies:

```bash
npm install
```

2. Create `.env` from `.env.example`:

```bash
copy .env.example .env
```

2. If using GROQ, add your API key to `.env`:

```text
GROQ_API_KEY=your_groq_api_key_here
```

4. Start the development server:

```bash
npm run dev
```

5. Open the app in your browser:

```text
http://localhost:3000
```

## File structure

- `app/page.tsx` — frontend dashboard and search form
- `app/api/search/route.ts` — aggregator endpoint
- `app/api/respond/route.ts` — response generation endpoint
- `lib/mockData.ts` — seeded review and mention data
- `lib/analysis.ts` — sentiment/topic/emotion analysis and summary builder
- `lib/ai.ts` — GROQ wrapper + fallback response generator

## Notes

- This repository is intentionally designed to be modular.
- The mock data and simple analytics can be replaced by real connectors and NLP services without changing the frontend.
- The current implementation is safe and respects the requirement to avoid unsafe scraping.
