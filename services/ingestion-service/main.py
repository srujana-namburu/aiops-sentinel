# import os
# from typing import Optional
# import uvicorn
# from dotenv import load_dotenv
# from fastapi import FastAPI, HTTPException, Request
# from openai import OpenAI
# from pydantic import BaseModel
# from prometheus_fastapi_instrumentator import Instrumentator

# from logger import get_logger


# class AnalyzeRequest(BaseModel):
#     incident_id: str
#     correlation_id: str
#     agent: str
#     prompt: str
#     duration_ms: Optional[int] = None


# class AnalyzeResponse(BaseModel):
#     incident_id: str
#     correlation_id: str
#     agent: str
#     model: str
#     output: str


# # Load environment variables (e.g., .env) before app initialization
# # Ensure we load the workspace root .env even when running from a subdirectory.
# from pathlib import Path

# root_env = Path(__file__).resolve().parents[2] / ".env"
# # Fallback to current working directory if root .env isn't found (for local testing)
# if not root_env.exists():
#     root_env = Path.cwd() / ".env"

# load_dotenv(dotenv_path=root_env)

# SERVICE_NAME = "ingestion-service"
# logger = get_logger(service=SERVICE_NAME)

# app = FastAPI(title=SERVICE_NAME)

# # Prometheus instrumentation must be registered before the app starts.
# instrumentator = Instrumentator()
# instrumentator.instrument(app).expose(app)

# openai_client: Optional[OpenAI] = None


# @app.on_event("startup")
# async def on_startup() -> None:
#     # Ensure OpenAI is configured (via OPENAI_API_KEY env var)
#     global openai_client
#     openai_api_key = os.getenv("OPENAI_API_KEY")
#     if not openai_api_key:
#         logger.warning(
#             "OPENAI_API_KEY not set; GPT calls will fail.",
#             extra={"incident_id": None, "correlation_id": None, "agent": None},
#         )
#         openai_client = None
#         return

#     openai_client = OpenAI(api_key=openai_api_key)


# @app.get("/health")
# async def health() -> dict:
#     """Health check endpoint."""
#     logger.info(
#         "Health check",
#         extra={"incident_id": None, "correlation_id": None, "agent": None},
#     )
#     return {"status": "ok"}


# @app.post("/incidents/analyze", response_model=AnalyzeResponse)
# async def analyze_incident(request: AnalyzeRequest) -> AnalyzeResponse:
#     """Analyze an incident using GPT-4o and return the generated output."""

#     logger.info(
#         "Received analyze request",
#         extra={
#             "incident_id": request.incident_id,
#             "correlation_id": request.correlation_id,
#             "agent": request.agent,
#             "duration_ms": request.duration_ms,
#         },
#     )

#     if not openai_client:
#         raise HTTPException(status_code=500, detail="OpenAI API key not configured")

#     model = "gpt-4o"
#     try:
#         completion = openai_client.chat.completions.create(
#             model=model,
#             messages=[
#                 {"role": "system", "content": "You are an incident analysis assistant."},
#                 {"role": "user", "content": request.prompt},
#             ],
#             max_tokens=1024,
#         )

#         # The OpenAI Python client may return either:
#         # - completion.choices[0].message.content (newer interface)
#         # - completion.choices[0].message["content"] (dictionary-like)
#         choice = completion.choices[0]
#         output = getattr(choice.message, "content", None) or choice.message.get("content")
#         if isinstance(output, list) and output:
#             output = output[0]
#         output = (output or "").strip()

#         logger.info(
#             "Generated analysis",
#             extra={
#                 "incident_id": request.incident_id,
#                 "correlation_id": request.correlation_id,
#                 "agent": request.agent,
#                 "duration_ms": request.duration_ms,
#             },
#         )

#         return AnalyzeResponse(
#             incident_id=request.incident_id,
#             correlation_id=request.correlation_id,
#             agent=request.agent,
#             model=model,
#             output=output,
#         )

#     except Exception as e:
#         logger.error(
#             "GPT call failed",
#             extra={
#                 "incident_id": request.incident_id,
#                 "correlation_id": request.correlation_id,
#                 "agent": request.agent,
#                 "duration_ms": request.duration_ms,
#                 "error": str(e),
#             },
#         )
#         raise HTTPException(status_code=500, detail="Failed to analyze incident")


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))

# main.py
# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from prometheus_fastapi_instrumentator import Instrumentator
from dotenv import load_dotenv
from logger import get_logger
import os
import time
from contextlib import asynccontextmanager
from database import engine, Base, Incident, get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from kafka_producer import send_incident
# Load env variables
load_dotenv()

# Initialize logger
logger = get_logger("ingestion-service")

# Create FastAPI app
#app = FastAPI(title="Ingestion Service")
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Ingestion Service", lifespan=lifespan)
# Enable CORS (frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus metrics endpoint
Instrumentator().instrument(app).expose(app)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class IncidentEvent(BaseModel):
    service_name: str
    error_message: str
    error_count: int


# Health check
@app.get("/health")
def health():
    return {"status": "ok", "service": "ingestion-service"}


# AI Analysis endpoint
@app.post("/incidents/analyze")
def analyze(event: IncidentEvent):
    start_time = time.time()

    logger.info(
        "Analyzing incident",
        extra={"service_name": event.service_name}
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an expert SRE. Analyze incidents."
            },
            {
                "role": "user",
                "content": f"Service: {event.service_name}, Error: {event.error_message}"
            }
        ]
    )

    analysis = response.choices[0].message.content

    # Calculate latency
    duration = (time.time() - start_time) * 1000

    logger.info(
        "Analysis complete",
        extra={
            "service_name": event.service_name,
            "duration_ms": round(duration, 2)
        }
    )

    # Improved structured response
    return {
        "service": event.service_name,
        "analysis": analysis,
        "severity": "high" if event.error_count > 10 else "low"
    }
@app.post("/incidents")
def create_incident(event: IncidentEvent):

    send_incident(event.dict())

    return {
        "message": "Incident sent to processing pipeline",
        "status": "QUEUED"
    }

@app.get("/incidents")
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).order_by(Incident.created_at.desc()).limit(50).all()


@app.get("/incidents/{incident_id}")
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    return db.query(Incident).filter(Incident.id == incident_id).first()

@app.get("/incidents/display/{display_id}")
def get_by_display_id(display_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.display_id == display_id).first()

    if not incident:
        return {"error": "Incident not found"}

    return incident