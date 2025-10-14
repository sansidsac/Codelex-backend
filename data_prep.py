
"""
Preprocess Kannada → Python dataset for CodeT5 fine-tuning.
- Loads JSON dataset with columns: 'kannada text', 'code', 'text'
- Splits into train/validation
- Tokenizes using CodeT5 tokenizer
- Saves tokenized dataset to disk
"""

import os
import sys

# Error handling for required packages
try:
    from datasets import load_dataset, DatasetDict
    from transformers import AutoTokenizer
except ImportError as e:
    print("❌ Required package missing:", e)
    print("Install with: pip install transformers datasets sentencepiece protobuf")
    sys.exit(1)

DATA_PATH = "lang_dataset.json"
MODEL_NAME = "Salesforce/codet5-small"
TOKENIZED_PATH = "tokenized_kannada_dataset"

# Load JSON dataset
dataset = load_dataset("json", data_files=DATA_PATH)

# Split train/validation (90/10)
if "train" not in dataset:
    dataset = dataset["train"].train_test_split(test_size=0.1)
    dataset = DatasetDict({
        "train": dataset["train"],
        "validation": dataset["test"]
    })

print("✅ Loaded dataset splits:", list(dataset.keys()))

# Load CodeT5 tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Preprocessing function for seq2seq
def preprocess_function(examples):
    inputs = examples["kannada text"]
    targets = examples["code"]
    model_inputs = tokenizer(
        inputs, max_length=128, truncation=True, padding="max_length"
    )
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            targets, max_length=128, truncation=True, padding="max_length"
        )
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Tokenize dataset
tokenized_dataset = dataset.map(preprocess_function, batched=True, remove_columns=dataset["train"].column_names)

# Save tokenized dataset
tokenized_dataset.save_to_disk(TOKENIZED_PATH)
print(f"✅ Tokenized dataset saved to '{TOKENIZED_PATH}'")