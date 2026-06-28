import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.feedback_store import save_feedback
from app.knowledge import all_sources
from app.models import ChatRequest, ChatResponse, FeedbackRequest
from app.rag_pipeline import RAGPipeline
from app.sanitize import sanitize_query

RATE_LIMIT_PER_HOUR = os.environ.get("RATE_LIMIT_PER_HOUR", "30")

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Hanuman Ji API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline: RAGPipeline | None = None


@app.on_event("startup")
def load_pipeline():
    global pipeline
    pipeline = RAGPipeline()
    _start_kavacha_monitoring(pipeline)


def _start_kavacha_monitoring(target: RAGPipeline) -> None:
    """Wires Hanuman Ji into Kavacha (the sibling infra project that monitors
    it) -- a no-op until KAVACHA_API_KEY/KAVACHA_PROJECT_ID are set, so a
    fresh clone runs fine without ever registering a project."""
    api_key = os.environ.get("KAVACHA_API_KEY")
    project_id = os.environ.get("KAVACHA_PROJECT_ID")
    if not (api_key and project_id):
        return
    import kavacha

    kavacha.init(api_key=api_key, project_id=project_id, base_url=os.environ.get("KAVACHA_API_URL"))
    kavacha.watch(target)


@app.get("/api/health")
def health():
    return {"status": "ok", "pipeline_loaded": pipeline is not None}


@app.get("/api/sources")
def sources():
    return all_sources()


@app.post("/api/chat", response_model=ChatResponse)
@limiter.limit(f"{RATE_LIMIT_PER_HOUR}/hour")
def chat(payload: ChatRequest, request: Request):
    clean_query = sanitize_query(payload.query)
    result = pipeline.invoke(
        query=clean_query,
        language=payload.language,
        conversation_id=payload.conversation_id,
    )
    return result


@app.post("/api/feedback")
def feedback(payload: FeedbackRequest):
    save_feedback(payload.message_id, payload.rating, payload.comment)
    return {"status": "received"}
