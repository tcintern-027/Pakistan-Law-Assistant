from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.chat import router as chat_router
from backend.app.routes.health import router as health_router


app = FastAPI(
    title="Pakistan Law Assistant API",
    description=(
        "AI-powered legal information assistant using "
        "hybrid retrieval and grounded RAG."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "Pakistan Law Assistant API",
        "status": "running",
    }