"""
FastAPI Backend for Codelex - Regional Language to Python Code Generator
Supports: Kannada to Python code conversion with multi-stage pipeline
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import sys
from pathlib import Path

# Import model utilities
from model_service import ModelService

app = FastAPI(
    title="Codelex API",
    description="Convert regional language algorithms to Python code",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model service
model_service = None

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global model_service
    print("🚀 Starting Codelex API...")
    print("📦 Loading AI models...")
    model_service = ModelService()
    print("✅ Models loaded successfully!")

# Request/Response Models
class ProcessRequest(BaseModel):
    inputText: str
    inputLanguage: str = "kn"  # Kannada by default
    
class ProcessResponse(BaseModel):
    preprocess: str
    translation: str
    pseudo_code: str
    code: str
    execution: str
    feedback: str

class HealthResponse(BaseModel):
    status: str
    message: str
    model_loaded: bool

# API Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Codelex API is running",
        "model_loaded": model_service is not None and model_service.is_loaded()
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy" if model_service and model_service.is_loaded() else "unhealthy",
        "message": "All systems operational" if model_service and model_service.is_loaded() else "Model not loaded",
        "model_loaded": model_service is not None and model_service.is_loaded()
    }

@app.post("/api/process", response_model=ProcessResponse)
async def process_code(request: ProcessRequest):
    """
    Main endpoint to process regional language input through all stages:
    1. Preprocessing
    2. Translation to English
    3. Pseudo-code generation
    4. Python code generation
    5. Execution (placeholder for now)
    6. Feedback generation
    """
    if not model_service or not model_service.is_loaded():
        raise HTTPException(status_code=503, detail="Model service not available")
    
    if not request.inputText or not request.inputText.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")
    
    try:
        # Process through all stages
        result = model_service.process_pipeline(
            input_text=request.inputText,
            language=request.inputLanguage
        )
        return result
    
    except Exception as e:
        print(f"❌ Processing error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/api/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": [
            {"code": "kn", "name": "Kannada", "nativeName": "ಕನ್ನಡ"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
