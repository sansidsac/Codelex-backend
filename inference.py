from transformers import AutoTokenizer, T5ForConditionalGeneration
from deep_translator import GoogleTranslator

MODEL_PATH = "./kannada_python_t5_model"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)
def translate_kannada_to_english(kannada_text):
    return GoogleTranslator(source='kn', target='en').translate(kannada_text)

def generate_code(kannada_instruction):
    inputs = tokenizer(kannada_instruction, return_tensors="pt", truncation=True, max_length=128)
    output_ids = model.generate(**inputs, max_length=128, num_beams=4)
    code = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return code

if __name__ == "__main__":
    kannada_text = input("Enter Kannada instruction: ")
    english_text = translate_kannada_to_english(kannada_text)
    print("\n🔎 Translated to English:\n", english_text)
    
    python_code = generate_code(kannada_text)
    print("\nGenerated Python code:\n")
    print(python_code)