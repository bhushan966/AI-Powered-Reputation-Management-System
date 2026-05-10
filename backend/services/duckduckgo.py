import asyncio
from ddgs import DDGS

def _sync_search(query: str) -> list[str]:
    """Synchronous DuckDuckGo search (runs in a thread)."""
    snippets = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=10):
            if r.get("body"):
                snippets.append(r["body"])
            if r.get("title"):
                snippets.append(r["title"])
    return snippets[:15]

async def search_web(query: str) -> list[str]:
    """
    Search DuckDuckGo using the duckduckgo-search v8 API.
    DDGS is synchronous in v8+; we run it in a thread to stay async-safe.
    Returns a list of snippet strings (body + title from results).
    """
    try:
        snippets = await asyncio.to_thread(_sync_search, query)
        print(f"[DDG] Got {len(snippets)} snippets for: {query}")
        return snippets
    except Exception as e:
        print(f"[DDG] Error during search: {e}")
        return []
