"""
AI Text Analyzer API — Your first production-style AI service.

This is a FastAPI service that wraps an LLM API call behind a clean REST endpoint.
It demonstrates: proper project structure, error handling, logging, type safety,
and the pattern you'll use for every AI service you build from here on.
"""


import logging
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# --- Logging setup (every production service needs this) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# --- App initialization ---
app = FastAPI(
    title="AI Text Analyzer",
    description="A production-style AI service — Phase 1 of the AI Engineer roadmap.",
    version="0.1.0",
)


# --- Request/Response models (always define these explicitly) ---
class AnalyzeRequest(BaseModel):
    """What the client sends us."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The text to analyze.",
        examples=["The new product launch exceeded our Q3 targets by 40%."],
    )


class AnalyzeResponse(BaseModel):
    """What we send back."""

    summary: str
    word_count: int
    sentiment: str
    processed_at: str


# --- Health check (every production service has one) ---
@app.get("/health")
async def health_check() -> dict:
    """Used by monitoring systems to verify the service is alive."""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/version")
async def get_version() -> dict:
    """Return the current API version."""
    return{"version": app.version,"title": app.title}

# --- Main endpoint ---
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze input text and return a summary, word count, and sentiment.

    For now this uses rule-based logic. In Phase 2, you'll swap this
    for an actual LLM API call — the endpoint stays the same, only the
    internal implementation changes. That's the point of good architecture.
    """
    logger.info("Received analyze request | text_length=%d", len(request.text))

    try:
        words = request.text.split()
        word_count = len(words)

        # Simple extractive summary (first 30 words)
        summary = " ".join(words[:30])
        if word_count > 30:
            summary += "..."

        # Rule-based sentiment (placeholder — you'll replace with LLM)
        positive_words = {"great", "excellent", "good", "exceeded", "success", "amazing", "love"}
        negative_words = {"bad", "terrible", "failed", "poor", "awful", "hate", "worst"}

        text_lower = request.text.lower()
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)

        if pos_count > neg_count:
            sentiment = "positive"
        elif neg_count > pos_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        response = AnalyzeResponse(
            summary=summary,
            word_count=word_count,
            sentiment=sentiment,
            processed_at=datetime.now(timezone.utc).isoformat(),
        )

        logger.info(
            "Analysis complete | words=%d sentiment=%s",
            word_count,
            sentiment,
        )
        return response

    except Exception as e:
        logger.error("Analysis failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Analysis failed") from e
