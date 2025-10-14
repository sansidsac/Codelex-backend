from transformers import AutoTokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import load_from_disk, DatasetDict
from transformers import DataCollatorForSeq2Seq

# Load tokenized dataset
dataset = load_from_disk("tokenized_kannada_dataset")

# If only "train" split exists, create a "test" split from it
if "train" in dataset and "test" not in dataset:
    # Split 10% for validation
    train_test = dataset["train"].train_test_split(test_size=0.1)
    dataset = DatasetDict({
        "train": train_test["train"],
        "test": train_test["test"]
    })

# Ensure dataset splits exist and are Dataset objects
if "train" not in dataset or "test" not in dataset:
    raise ValueError("Dataset must contain 'train' and 'test' splits.")

# Check required columns
required_columns = {"input_ids", "attention_mask", "labels"}
for split in ["train", "test"]:
    if not required_columns.issubset(set(dataset[split].column_names)):
        raise ValueError(f"Dataset split '{split}' must contain columns: {required_columns}")

# Load tokenizer and model
model_name = "Salesforce/codet5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Training configuration
import torch
training_args = TrainingArguments(
    output_dir="./results",
    do_train=True,
    do_eval=True,
    learning_rate=5e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=50,
    save_total_limit=2,
    fp16=torch.cuda.is_available(),
)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    data_collator=data_collator,  # <-- add this line
)

print("🚀 Training started...")
trainer.train()

# Save model + tokenizer after training
model.save_pretrained("./kannada_python_t5_model")
tokenizer.save_pretrained("./kannada_python_t5_model")

print("✅ Model training completed and saved successfully!")
