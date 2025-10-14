# Kannada → Python Code Translator using CodeT5

This project builds a tool to convert algorithmic instructions written in Kannada into Python code using a fine-tuned Salesforce CodeT5 model.  
It includes scripts for data preprocessing, model training, and inference.

## Features

- **Data Preprocessing:** Tokenizes Kannada instructions and Python code for training.
- **Model Training:** Fine-tunes CodeT5 on your custom dataset.
- **Inference:** Translates new Kannada instructions to Python code.

## Folder Structure

```
final-year-project/
│
├── data_prep.py
├── train_model.py
├── inference.py
├── lang_dataset.json
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/ig-quinzel/final-year-project.git
   cd final-year-project
   ```

2. **Create and activate a Python virtual environment:**
   - On Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Prepare the dataset:**
   - Make sure `lang_dataset.json` is present in the project folder.
   - Run the data preprocessing script:
     ```
     python data_prep.py
     ```

5. **Train the model:**
   ```
   python train_model.py
   ```

6. **Run inference:**
   ```
   python inference.py
   ```
   - Enter a Kannada instruction when prompted to get the generated Python code.

## Requirements

See `requirements.txt` for all Python dependencies.

---
