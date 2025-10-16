# Codelex Backend - Regional Language to Python Code Converter

FastAPI backend for converting algorithmic instructions written in Kannada into Python code using a fine-tuned Salesforce CodeT5 model.

## Features

- **Multi-stage Processing Pipeline:**
  - Text Preprocessing & Normalization
  - Translation to English (Kannada → English)
  - Pseudo-code Generation
  - Python Code Generation (using fine-tuned CodeT5)
  - Execution (coming soon)
  - AI Feedback & Suggestions

- **RESTful API:** FastAPI server with CORS support for frontend integration
- **Model Training:** Fine-tune CodeT5 on custom Kannada-Python datasets
- **Inference:** Real-time translation of Kannada instructions to Python code

## Folder Structure

```
Codelex-backend/
│
├── api.py                          # FastAPI server
├── model_service.py                # AI model service & pipeline
├── data_prep.py                    # Dataset preprocessing
├── train_model.py                  # Model training script
├── inference.py                    # CLI inference tool
├── lang_dataset.json               # Training dataset
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Setup Instructions

### 1. Clone the repository:
```bash
git clone https://github.com/sansidsac/Codelex-backend.git
cd Codelex-backend
```

### 2. Create and activate a Python virtual environment:

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Run the API Server (Recommended for Frontend Integration)

1. **Start the FastAPI server:**
```bash
python api.py
```

Or with uvicorn directly:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

2. **API will be available at:**
- API Base: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

3. **Test the API:**
```bash
# Health check
curl http://localhost:8000/health

# Process Kannada text
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{"inputText": "1 ರಿಂದ 10 ರವರೆಗೆ ಸಂಖ್ಯೆಗಳನ್ನು ಮುದ್ರಿಸಿ", "inputLanguage": "kn"}'
```

### Option 2: Train Your Own Model (Optional)

4. **Prepare the dataset:**
   - Ensure `lang_dataset.json` is present
   - Run data preprocessing:
     ```bash
     python data_prep.py
     ```

5. **Train the model:**
   ```bash
   python train_model.py
   ```

### Option 3: Command Line Inference

6. **Run inference via CLI:**
   ```bash
   python inference.py
   ```
   - Enter a Kannada instruction when prompted to get the generated Python code.

## API Endpoints

### `GET /` or `GET /health`
Health check endpoint
- Returns: `{ status, message, model_loaded }`

### `POST /api/process`
Main processing endpoint - converts Kannada to Python code
- **Request Body:**
  ```json
  {
    "inputText": "1 ರಿಂದ 10 ರವರೆಗೆ ಸಂಖ್ಯೆಗಳನ್ನು ಮುದ್ರಿಸಿ",
    "inputLanguage": "kn"
  }
  ```
- **Response:**
  ```json
  {
    "preprocess": "Input tokenized: 5 tokens found and normalized",
    "translation": "Print numbers from 1 to 10",
    "pseudo_code": "FOR i FROM 1 TO 10\n    PRINT i\nEND FOR",
    "code": "for i in range(1, 11):\n    print(i)",
    "execution": "# Code execution not yet implemented",
    "feedback": "✓ Good use of for loop with range() function"
  }
  ```

### `GET /api/languages`
Get list of supported languages
- Returns: Array of supported languages with codes

## Frontend Integration

Update your frontend API service to point to: `http://localhost:8000`

Example (in `web/src/services/mockAPI.ts`):
```typescript
const API_BASE_URL = 'http://localhost:8000';

export const api = {
  async processCode(inputText: string, language: string) {
    const response = await fetch(`${API_BASE_URL}/api/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ inputText, inputLanguage: language })
    });
    return response.json();
  }
};
```

## Requirements

See `requirements.txt` for all Python dependencies.

## Current Features ✅

- ✅ FastAPI REST API server
- ✅ Kannada to English translation
- ✅ Multi-line Python code generation
- ✅ Pseudo-code generation
- ✅ AI feedback and suggestions
- ✅ CORS enabled for frontend

## Coming Soon 🚧

- 🚧 Live Python code execution (sandboxed)
- 🚧 Support for more regional languages
- 🚧 Enhanced error handling
- 🚧 Code optimization suggestions

---

