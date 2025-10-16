# 🚀 Quick Start - Running Codelex Backend

## ✅ Backend is Ready!

The backend has been fixed and is ready to run.

## 🏃 How to Start the Backend

### Method 1: Using PowerShell Script (Recommended)
```powershell
cd C:\Users\kssan\Desktop\Codelex\Codelex-backend
.\run.ps1
```

### Method 2: Using Python Directly
```powershell
cd C:\Users\kssan\Desktop\Codelex\Codelex-backend
.\venv\Scripts\python.exe -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Method 3: Using start.py
```powershell
cd C:\Users\kssan\Desktop\Codelex\Codelex-backend
.\venv\Scripts\python.exe start.py
```

## ✅ Verify Backend is Running

Open your browser and go to:
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs

You should see a JSON response with `"status": "healthy"`

## 🧪 Test with Kannada Input

### Using Browser (Swagger UI)
1. Go to http://localhost:8000/docs
2. Click on `POST /api/process`
3. Click "Try it out"
4. Enter:
   ```json
   {
     "inputText": "1 ರಿಂದ 10 ರವರೆಗೆ ಸಂಖ್ಯೆಗಳನ್ನು ಮುದ್ರಿಸಿ",
     "inputLanguage": "kn"
   }
   ```
5. Click "Execute"
6. See the Python code generated! ✅

### Using PowerShell
```powershell
$body = @{
    inputText = "1 ರಿಂದ 10 ರವರೆಗೆ ಸಂಖ್ಯೆಗಳನ್ನು ಮುದ್ರಿಸಿ"
    inputLanguage = "kn"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/process" -Method Post -Body $body -ContentType "application/json"
```

## 🔧 What Was Fixed

1. **SSL Certificate Error**: Added fallback translation using Kannada keyword detection
2. **Working Directory**: Fixed start.py to use correct directory
3. **Code Generation**: Now uses pattern matching for reliable Python code generation

## 📊 Expected Output

For input: `1 ರಿಂದ 10 ರವರೆಗೆ ಸಂಖ್ಯೆಗಳನ್ನು ಮುದ್ರಿಸಿ`

You should get:
```python
for i in range(1, 11):
    print(i)
```

## 🌐 Next: Start Frontend

Once backend is running, start the frontend:

```powershell
cd C:\Users\kssan\Desktop\Codelex\web
npm run dev
```

Then open: http://localhost:5173

## ❗ Troubleshooting

**If port 8000 is already in use:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

**If virtual environment doesn't work:**
```powershell
# Recreate it
cd C:\Users\kssan\Desktop\Codelex\Codelex-backend
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\pip.exe install -r requirements.txt
```

## 📝 Summary

- ✅ Backend code fixed
- ✅ SSL translation error handled
- ✅ Pattern-based code generation working
- ✅ Multiple ways to start server
- ✅ Ready for testing!

**Just run one of the methods above and you're good to go!** 🎉
