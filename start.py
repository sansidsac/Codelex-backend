#!/usr/bin/env python3
"""
Startup script for Codelex Backend API
Checks dependencies and starts the FastAPI server
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'transformers',
        'deep_translator',
        'torch'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\n💡 Install with: pip install -r requirements.txt")
        return False
    
    return True

def check_model():
    """Check if model exists"""
    model_path = "./kannada_python_t5_model"
    if not os.path.exists(model_path):
        print(f"⚠️  Model not found at {model_path}")
        print("💡 The system will use the base CodeT5 model instead.")
        print("   To use a fine-tuned model, run: python train_model.py")
        return True  # Not critical, can continue with base model
    
    print(f"✅ Model found at {model_path}")
    return True

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting Codelex API Server...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API Docs at: http://localhost:8000/docs")
    print("\nPress CTRL+C to stop the server\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "api:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        sys.exit(0)

if __name__ == "__main__":
    print("=" * 60)
    print("  CODELEX BACKEND - Regional Language to Python Converter")
    print("=" * 60)
    print()
    
    # Change to script directory to ensure correct imports
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies installed")
    
    # Check model
    print("\n🔍 Checking model...")
    check_model()
    
    # Start server
    start_server()
