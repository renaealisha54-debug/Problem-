import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from build_manager import router as build_router
from middleware.auth import APIKeyMiddleware
from middleware.rate_limiter import RateLimiterMiddleware
from middleware.logger import LoggerMiddleware
from models.schemas import CodeRequest
from services.ai_service import correct_code, convert_code, explain_code
from sandbox.executor import run_code_safely

load_dotenv()
os.makedirs("logs", exist_ok=True)
os.makedirs("builds", exist_ok=True)

app = FastAPI(title="ProblemCode API", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_middleware(RateLimiterMiddleware, max_requests=30, window_seconds=60)
app.add_middleware(LoggerMiddleware)
app.add_middleware(APIKeyMiddleware)

app.include_router(build_router)

if os.path.exists("downloads"):
    app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/api/execute")
async def execute_code(request: CodeRequest):
    return run_code_safely(request.code, request.language)

@app.post("/api/ai/correct")
async def ai_correct(request: CodeRequest):
    try:
        result = correct_code(request.code, request.language)
        return {"corrected_code": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/convert")
async def ai_convert(request: CodeRequest):
    try:
        converted, new_lang = convert_code(request.code, request.language)
        return {"converted_code": converted, "new_language": new_lang}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/explain")
async def ai_explain(request: CodeRequest):
    try:
        explanation = explain_code(request.code, request.language)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
