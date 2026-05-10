from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from services.ai_engine import generate_live_reviews, analyze_reviews, generate_response

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchPayload(BaseModel):
    businessName: str
    location: str
    website: str | None = None

class RespondPayload(BaseModel):
    reviewText: str
    sentiment: str

@app.post("/api/search")
async def search_endpoint(payload: SearchPayload):
    try:
        raw_data = await generate_live_reviews(payload.businessName, payload.location)
        result = analyze_reviews(payload.businessName, payload.location, raw_data)
        return result
    except Exception as e:
        print(f"Error in /api/search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/respond")
async def respond_endpoint(payload: RespondPayload):
    try:
        response_text = await generate_response(payload.reviewText, payload.sentiment)
        return {"response": response_text}
    except Exception as e:
        print(f"Error in /api/respond: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
