
import os
import re
import secrets
import logging
import time

from pathlib import Path
from contextlib import asynccontextmanager

from dotenv import load_dotenv

from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Depends,
    Request
)

from pydantic import BaseModel, Field

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from fastembed import TextEmbedding

from src.rag.document_loader import load_documents
from src.rag.text_chunker import create_document_chunks
from src.rag.hybrid_retriever import hybrid_search

from src.triage.predict_ticket import predict_ticket
from src.triage.ticket_schema import TicketPrediction


# =====================================================
# 1. ENVIRONMENT CONFIGURATION
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("NEXUSAI_API_KEY")

if not API_KEY:
    raise RuntimeError("NEXUSAI_API_KEY is missing from .env")


# =====================================================
# 2. LOGGING CONFIGURATION
# =====================================================

LOG_FILE = PROJECT_ROOT / "nexusai.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger("NexusAI")


# =====================================================
# 3. RATE LIMITER
# =====================================================

limiter = Limiter(key_func=get_remote_address)


# =====================================================
# 4. GREETING DETECTION
# =====================================================

GREETINGS = {
    "hi",
    "hello",
    "hey",
    "hey there",
    "hi there",
    "hello there",
    "good morning",
    "good afternoon",
    "good evening",
    "how are you",
    "how are you doing",
    "thanks",
    "thank you"
}


def is_greeting(message: str) -> bool:

    normalized = re.sub(
        r"[^\w\s]",
        "",
        message.lower()
    ).strip()

    normalized = " ".join(normalized.split())

    return normalized in GREETINGS


# =====================================================
# 5. LOAD RAG SYSTEM AT STARTUP
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Loading NexusAI RAG system...")

    documents = load_documents(PROJECT_ROOT / "docs")

    chunks = create_document_chunks(documents)

    model = TextEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    app.state.documents = documents
    app.state.chunks = chunks
    app.state.embedding_model = model

    logger.info("RAG system loaded successfully!")
    logger.info("Total documents: %s", len(documents))
    logger.info("Total chunks: %s", len(chunks))

    yield

    logger.info("NexusAI shutting down...")


# =====================================================
# 6. FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="NexusAI API",
    description="Intelligent Support Assistant with RAG and Ticket Intelligence",
    version="1.2.1",
    lifespan=lifespan
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


# =====================================================
# 7. REQUEST LOGGING MIDDLEWARE
# =====================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        "Method: %s | Path: %s | Status: %s | Time: %.4f seconds",
        request.method,
        request.url.path,
        response.status_code,
        process_time
    )

    return response


# =====================================================
# 8. REQUEST AND RESPONSE MODELS
# =====================================================

class HealthResponse(BaseModel):
    status: str
    project: str


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=1000,
        description="Enter a support question or greeting"
    )


class TicketRequest(BaseModel):
    ticket: str = Field(
        min_length=5,
        max_length=2000
    )


# =====================================================
# 9. API KEY AUTHENTICATION
# =====================================================

def verify_api_key(
    x_api_key: str = Header(default=None)
):

    if not x_api_key or not secrets.compare_digest(
        x_api_key,
        API_KEY
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

    return x_api_key


# =====================================================
# 10. HOME ENDPOINT
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to NexusAI!",
        "status": "running"
    }


# =====================================================
# 11. HEALTH CHECK ENDPOINT
# =====================================================

@app.get("/health", response_model=HealthResponse)
def health_check():

    return {
        "status": "healthy",
        "project": "NexusAI"
    }


# =====================================================
# 12. RAG QUESTION-ANSWERING ENDPOINT
# =====================================================

@app.post("/ask")
@limiter.limit("5/minute")
def ask_question(
    request: Request,
    question_request: QuestionRequest,
    api_key: str = Depends(verify_api_key)
):

    question = question_request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # Handle greetings before document retrieval

    if is_greeting(question):

        logger.info("Greeting detected: %s", question)

        return {
            "question": question,
            "answer": (
                "Hello! Welcome to NexusAI. "
                "I'm your AI support assistant. "
                "I can help you with account access, "
                "password resets, billing, payments "
                "and subscriptions. How can I assist you today?"
            ),
            "citations": [],
            "status": "greeting"
        }

    try:

        results = hybrid_search(
            query=question,
            chunks=request.app.state.chunks,
            model=request.app.state.embedding_model,
            user_role="user",
            top_k=1
        )

        if not results:

            return {
                "question": question,
                "answer": (
                    "I could not find relevant information "
                    "in the available support documents. "
                    "Please try rephrasing your question "
                    "or contact the support team."
                ),
                "citations": [],
                "status": "no_results"
            }

        answer = "\n\n".join(
            result["text"] for result in results
        )

        citations = [
            {
                "filename": result["filename"],
                "source": result["source"],
                "chunk_number": result["chunk_number"],
                "page": result["page"],
                "score": result["score"]
            }
            for result in results
        ]

        return {
            "question": question,
            "answer": answer,
            "citations": citations,
            "status": "success"
        }

    except Exception:

        logger.exception("RAG retrieval failed")

        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving information."
        )


# =====================================================
# 13. SUPPORT TICKET TRIAGE ENDPOINT
# =====================================================

@app.post(
    "/triage",
    response_model=TicketPrediction
)
@limiter.limit("5/minute")
def triage_ticket(
    request: Request,
    ticket_request: TicketRequest,
    api_key: str = Depends(verify_api_key)
):

    try:

        result = predict_ticket(
            ticket_request.ticket
        )

        logger.info(
            "Support ticket classified successfully"
        )

        return result

    except Exception:

        logger.exception(
            "Ticket classification failed"
        )

        raise HTTPException(
            status_code=500,
            detail="Ticket classification failed."
        )
