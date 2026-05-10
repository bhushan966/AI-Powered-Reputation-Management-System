import os
import json
import httpx
from typing import List, Dict, Any
from .duckduckgo import search_web

async def generate_live_reviews(business_name: str, location: str) -> Dict[str, Any]:
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        raise Exception('GROQ_API_KEY is not configured in .env')

    # Fetch real-world facts from DuckDuckGo
    snippets = await search_web(f'"{business_name}" {location} reviews rating')
    snippets_text = "\n".join(snippets)

    prompt = f"""You are a helpful data API. The user is searching for reviews of the business "{business_name}" in "{location}". 
We have performed a live web search to get real-world data. Here are the search snippets:
---
{snippets_text}
---

Based STRICTLY on the real-world facts and ratings in the snippets above, return a JSON object with four keys:
1. "reviews": an array of exactly 6 highly realistic review objects. Do not use generic phrases. Base complaints and praises on the snippets.
2. "recommendations": an array of exactly 3 highly specific, actionable recommendations for the business owners. Each item MUST be a plain string.
3. "totalReviewCount": a number representing the estimated real-world total number of reviews this business has online (derive from snippets if possible, otherwise estimate realistically).
4. "averageRating": a number representing the overall real-world average rating out of 5.0 for this business (derive from snippets if possible).

Each review object must have the following string keys:
- "id": a unique string (e.g., "g-123")
- "source": a string (e.g., "Google Reviews", "TripAdvisor")
- "author": a string (a realistic reviewer name)
- "rating": a number from 1 to 5
- "message": a string (the review text, mention specific details)
- "publishedAt": a string (date in YYYY-MM-DD format)
- "sentiment": "Positive", "Neutral", or "Negative"
- "topic": a short, specific phrase describing the main subject
- "emotion": "Happy", "Impressed", "Frustrated", "Disappointed", or "Neutral"
- "priority": "High", "Medium", or "Low"

Return ONLY valid JSON."""

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.7,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {groq_key}',
                'Content-Type': 'application/json'
            },
            json=payload
        )
        
        if response.status_code != 200:
            print("Groq error:", response.text)
            raise Exception('Failed to fetch from Groq API')
            
        data = response.json()
        content = data['choices'][0]['message']['content']
        
        try:
            parsed = json.loads(content)
            return {
                "reviews": parsed.get("reviews", []),
                "recommendations": parsed.get("recommendations", []),
                "totalReviewCount": parsed.get("totalReviewCount"),
                "averageRating": parsed.get("averageRating")
            }
        except Exception as e:
            print("Parse error:", e, content)
            raise Exception('Failed to parse reviews from Groq')

def build_summary(reviews: List[Dict[str, Any]], ai_total_review_count: int = None, ai_average_rating: float = None) -> Dict[str, Any]:
    total_reviews = ai_total_review_count if ai_total_review_count is not None else len(reviews)
    
    calc_sum = sum(float(r.get("rating", 3)) for r in reviews)
    calc_avg = calc_sum / max(len(reviews), 1)
    average_rating = ai_average_rating if ai_average_rating is not None else calc_avg
    
    sentiment_split = {
        "positive": sum(1 for r in reviews if r.get("sentiment") == "Positive"),
        "neutral": sum(1 for r in reviews if r.get("sentiment") == "Neutral"),
        "negative": sum(1 for r in reviews if r.get("sentiment") == "Negative"),
    }
    
    complaint_topics = [r.get("topic", "General") for r in reviews if r.get("sentiment") != "Positive"]
    compliment_topics = [r.get("topic", "General") for r in reviews if r.get("sentiment") == "Positive"]
    
    top_complaints = list(dict.fromkeys(complaint_topics))[:5]
    top_compliments = list(dict.fromkeys(compliment_topics))[:5]
    
    return {
        "totalReviews": total_reviews,
        "averageRating": round(average_rating, 1),
        "sentimentSplit": sentiment_split,
        "topComplaints": top_complaints,
        "topCompliments": top_compliments,
    }

def analyze_reviews(business_name: str, location: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
    raw_reviews = raw_data.get("reviews", [])
    ai_recommendations = raw_data.get("recommendations", [])
    
    reviews = []
    for r in raw_reviews:
        # Fallback logic if needed
        sentiment = r.get("sentiment", "Neutral")
        topic = r.get("topic", "General")
        emotion = r.get("emotion", "Neutral")
        priority = r.get("priority", "Low")
        
        reviews.append({
            **r,
            "sentiment": sentiment,
            "topic": topic,
            "emotion": emotion,
            "priority": priority
        })
        
    summary = build_summary(reviews, raw_data.get("totalReviewCount"), raw_data.get("averageRating"))
    
    recommendations = ai_recommendations if len(ai_recommendations) > 0 else []
    if not recommendations:
        if summary["sentimentSplit"]["negative"] > 0:
            recommendations.append("Address slow service and staffing issues, especially around peak dinner hours.")
        if not recommendations:
            recommendations.append("Keep monitoring guest feedback and maintain strong service standards.")
            
    return {
        "businessName": business_name,
        "location": location,
        "reviews": reviews,
        "summary": summary,
        "recommendations": recommendations
    }

async def generate_response(review_text: str, sentiment: str) -> str:
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        raise Exception('GROQ_API_KEY is not configured in .env')

    prompt = f"""You are a professional reputation manager for a business.
Write a concise, professional reply to the following customer review.
The sentiment of the review is {sentiment}.

Review: "{review_text}"

Return only the response text. Do not include quotes or formatting."""

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {groq_key}',
                'Content-Type': 'application/json'
            },
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception('Failed to fetch from Groq API')
            
        data = response.json()
        return data['choices'][0]['message']['content']
