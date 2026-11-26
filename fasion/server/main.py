import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routers.algorithm import router as algorithm_router

app = FastAPI(
    title="Algorithm Backend Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

# CORS 설정 (Google Apps Script 연동 대비)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "dijkstra_navigation_server",
        "gemini_api_key_configured": bool(os.getenv("GEMINI_API_KEY"))
    }

app.include_router(algorithm_router)
