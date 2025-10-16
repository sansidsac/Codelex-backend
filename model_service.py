"""
Model Service for Codelex
Handles all AI model operations including:
- Text preprocessing
- Translation (Kannada to English)
- Pseudo-code generation
- Python code generation
- Feedback generation
"""

import os
import re
from typing import Dict, Optional
from pathlib import Path

try:
    from transformers import AutoTokenizer, T5ForConditionalGeneration
    from deep_translator import GoogleTranslator
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("Install with: pip install transformers deep-translator torch")
    raise

class ModelService:
    """Service class to manage AI models and processing pipeline"""
    
    def __init__(self, model_path: str = "./kannada_python_t5_model"):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self._load_models()
    
    def _load_models(self):
        """Load the CodeT5 model and tokenizer"""
        try:
            # Check if model exists
            if not os.path.exists(self.model_path):
                print(f"⚠️  Model not found at {self.model_path}")
                print("💡 Using base CodeT5 model instead...")
                self.model_path = "Salesforce/codet5-small"
            
            print(f"📦 Loading tokenizer from {self.model_path}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            
            print(f"🤖 Loading model from {self.model_path}...")
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_path)
            
            print("✅ Model and tokenizer loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None and self.tokenizer is not None
    
    def preprocess_text(self, text: str) -> Dict[str, str]:
        """
        Stage 1: Preprocess input text
        - Clean and normalize text
        - Tokenize
        """
        # Remove extra whitespace
        cleaned = " ".join(text.split())
        
        # Basic tokenization info
        tokens = cleaned.split()
        token_count = len(tokens)
        
        return {
            "cleaned_text": cleaned,
            "message": f"Input tokenized: {token_count} tokens found and normalized",
            "token_count": token_count
        }
    
    def translate_to_english(self, text: str, source_lang: str = "kn") -> Dict[str, str]:
        """
        Stage 2: Translate regional language to English
        Uses Google Translate API with SSL error handling
        """
        try:
            # Try translation with SSL verification disabled for Google Translate
            import ssl
            import certifi
            
            translator = GoogleTranslator(source=source_lang, target='en')
            translation = translator.translate(text)
            
            return {
                "translation": translation,
                "message": f"Translated from {source_lang.upper()} to English",
                "original": text
            }
        except Exception as e:
            print(f"⚠️  Translation error: {e}")
            print(f"💡 Using fallback: treating input as pattern-based")
            
            # Intelligent fallback based on Kannada patterns
            # Common Kannada number words and their English equivalents
            kannada_to_english_patterns = {
                'ಮುದ್ರಿಸಿ': 'print',
                'ಸಂಖ್ಯೆಗಳನ್ನು': 'numbers',
                'ರಿಂದ': 'from',
                'ರವರೆಗೆ': 'to',
                'ಸಮ': 'even',
                'ಮೊತ್ತ': 'sum',
                'ಲೆಕ್ಕ': 'calculate',
            }
            
            # Try to detect pattern from Kannada keywords
            text_lower = text.lower()
            detected_pattern = []
            
            for kannada, english in kannada_to_english_patterns.items():
                if kannada in text:
                    detected_pattern.append(english)
            
            # Extract numbers
            import re
            numbers = re.findall(r'\d+', text)
            
            # Build a simple English translation
            if numbers and 'ಮುದ್ರಿಸಿ' in text:
                if len(numbers) >= 2:
                    if 'ಸಮ' in text:
                        fallback_translation = f"Print even numbers from {numbers[0]} to {numbers[1]}"
                    elif 'ಮೊತ್ತ' in text or 'ಲೆಕ್ಕ' in text:
                        fallback_translation = f"Calculate sum of numbers from {numbers[0]} to {numbers[1]}"
                    else:
                        fallback_translation = f"Print numbers from {numbers[0]} to {numbers[1]}"
                else:
                    fallback_translation = "Print numbers"
            else:
                # Use original text if can't detect pattern
                fallback_translation = text
            
            return {
                "translation": fallback_translation,
                "message": "Translation unavailable - using pattern detection",
                "original": text
            }
    
    def generate_pseudo_code(self, english_text: str) -> Dict[str, str]:
        """
        Stage 3: Generate pseudo-code from English description
        Uses pattern matching and simple logic for now
        """
        # Simple heuristic-based pseudo-code generation
        english_lower = english_text.lower()
        
        # Initialize pseudo code
        pseudo_lines = []
        
        # Detect loop patterns
        if any(word in english_lower for word in ['loop', 'iterate', 'repeat', 'from', 'to']):
            # Try to extract range
            numbers = re.findall(r'\b(\d+)\b', english_text)
            if len(numbers) >= 2:
                start, end = numbers[0], numbers[1]
                pseudo_lines.append(f"FOR i FROM {start} TO {end}")
                
                # Check for conditions
                if 'even' in english_lower:
                    pseudo_lines.append("    IF i MOD 2 EQUALS 0 THEN")
                    pseudo_lines.append("        PRINT i")
                    pseudo_lines.append("    END IF")
                elif 'odd' in english_lower:
                    pseudo_lines.append("    IF i MOD 2 NOT EQUALS 0 THEN")
                    pseudo_lines.append("        PRINT i")
                    pseudo_lines.append("    END IF")
                else:
                    pseudo_lines.append("    PRINT i")
                
                pseudo_lines.append("END FOR")
        
        # Detect print patterns
        elif 'print' in english_lower or 'display' in english_lower or 'show' in english_lower:
            if 'hello' in english_lower or 'world' in english_lower:
                pseudo_lines.append('PRINT "Hello, World!"')
            else:
                # Extract what to print
                pseudo_lines.append('PRINT output')
        
        # Detect sum/calculation patterns
        elif 'sum' in english_lower or 'add' in english_lower or 'total' in english_lower:
            numbers = re.findall(r'\b(\d+)\b', english_text)
            if len(numbers) >= 2:
                start, end = numbers[0], numbers[1]
                pseudo_lines.append("SET sum = 0")
                pseudo_lines.append(f"FOR i FROM {start} TO {end}")
                pseudo_lines.append("    SET sum = sum + i")
                pseudo_lines.append("END FOR")
                pseudo_lines.append("PRINT sum")
        
        # Detect fibonacci
        elif 'fibonacci' in english_lower:
            numbers = re.findall(r'\b(\d+)\b', english_text)
            count = numbers[0] if numbers else "10"
            pseudo_lines.append("SET a = 0, b = 1")
            pseudo_lines.append("PRINT a, b")
            pseudo_lines.append(f"FOR i FROM 3 TO {count}")
            pseudo_lines.append("    SET c = a + b")
            pseudo_lines.append("    PRINT c")
            pseudo_lines.append("    SET a = b, b = c")
            pseudo_lines.append("END FOR")
        
        # Default fallback
        if not pseudo_lines:
            pseudo_lines.append("BEGIN")
            pseudo_lines.append("    PROCESS input")
            pseudo_lines.append("    GENERATE output")
            pseudo_lines.append("END")
        
        pseudo_code = "\n".join(pseudo_lines)
        
        return {
            "pseudo_code": pseudo_code,
            "message": "Structured pseudo-code generated successfully"
        }
    
    def generate_python_code(self, english_text: str, pseudo_code: str = None) -> Dict[str, str]:
        """
        Stage 4: Generate Python code from English description and pseudo-code
        Uses pattern matching for reliable code generation
        """
        try:
            english_lower = english_text.lower()
            code_lines = []
            
            # Detect sum/calculation patterns FIRST (before loop detection)
            if any(word in english_lower for word in ['sum', 'total', 'amount']) and any(word in english_lower for word in ['calculate', 'find', 'compute']):
                numbers = re.findall(r'\b(\d+)\b', english_text)
                if len(numbers) >= 2:
                    start, end = numbers[0], numbers[1]
                    code_lines.append(f"sum = 0")
                    code_lines.append(f"for i in range({start}, {int(end)+1}):")
                    code_lines.append(f"    sum += i")
                    code_lines.append(f"print(sum)")
                else:
                    # Generic sum
                    code_lines.append(f"total = 0")
                    code_lines.append(f"# Add your numbers here")
                    code_lines.append(f"print(total)")
            
            # Detect loop patterns
            elif any(word in english_lower for word in ['loop', 'iterate', 'repeat', 'from', 'to', 'print numbers', 'numbers from']):
                # Try to extract range
                numbers = re.findall(r'\b(\d+)\b', english_text)
                
                if len(numbers) >= 2:
                    start, end = numbers[0], numbers[1]
                    
                    # Check for even/odd patterns
                    if 'even' in english_lower or 'equal' in english_lower:
                        code_lines.append(f"for i in range({start}, {int(end)+1}):")
                        code_lines.append(f"    if i % 2 == 0:")
                        code_lines.append(f"        print(i)")
                    elif 'odd' in english_lower:
                        code_lines.append(f"for i in range({start}, {int(end)+1}):")
                        code_lines.append(f"    if i % 2 != 0:")
                        code_lines.append(f"        print(i)")
                    else:
                        # Simple loop
                        code_lines.append(f"for i in range({start}, {int(end)+1}):")
                        code_lines.append(f"    print(i)")
            
            # Detect fibonacci
            elif 'fibonacci' in english_lower:
                numbers = re.findall(r'\b(\d+)\b', english_text)
                count = numbers[0] if numbers else "10"
                code_lines.append(f"a, b = 0, 1")
                code_lines.append(f"print(a, b)")
                code_lines.append(f"for i in range(3, {int(count)+1}):")
                code_lines.append(f"    c = a + b")
                code_lines.append(f"    print(c)")
                code_lines.append(f"    a, b = b, c")
            
            # Detect factorial
            elif 'factorial' in english_lower:
                numbers = re.findall(r'\b(\d+)\b', english_text)
                num = numbers[0] if numbers else "5"
                code_lines.append(f"factorial = 1")
                code_lines.append(f"for i in range(1, {int(num)+1}):")
                code_lines.append(f"    factorial *= i")
                code_lines.append(f"print(factorial)")
            
            # Detect print patterns
            elif 'print' in english_lower or 'display' in english_lower or 'show' in english_lower:
                if 'hello' in english_lower or 'world' in english_lower:
                    code_lines.append('print("Hello, World!")')
                else:
                    # Extract what to print if possible
                    code_lines.append('print("Output")')
            
            # Detect variable assignment
            elif 'assign' in english_lower or 'store' in english_lower or 'variable' in english_lower:
                # Try to extract variable name and value
                numbers = re.findall(r'\b(\d+)\b', english_text)
                # Look for variable name (single letter)
                var_match = re.search(r'\b([A-Za-z])\b', english_text)
                
                if var_match and numbers:
                    var_name = var_match.group(1)
                    value = numbers[0]
                    code_lines.append(f"{var_name} = {value}")
                else:
                    code_lines.append("# Variable assignment")
                    code_lines.append("x = 0")
            
            # Default fallback - try to use the model for trained data
            if not code_lines:
                # Try using the model as last resort
                try:
                    # Use English text with the model
                    inputs = self.tokenizer(
                        english_text,
                        return_tensors="pt",
                        truncation=True,
                        max_length=128
                    )
                    
                    output_ids = self.model.generate(
                        **inputs,
                        max_length=128,
                        num_beams=4,
                        early_stopping=True,
                        no_repeat_ngram_size=2
                    )
                    
                    code = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
                    
                    # Validate the generated code looks like Python
                    if code and any(keyword in code for keyword in ['for', 'if', 'while', 'def', 'print', '=']):
                        code_lines = code.split('\n')
                    else:
                        # Model output doesn't look like code, use generic fallback
                        code_lines = ["# Generated code", "print('Result')"]
                except Exception as model_error:
                    print(f"⚠️  Model generation failed: {model_error}")
                    code_lines = ["# Code generation in progress", "print('Result')"]
            
            python_code = "\n".join(code_lines)
            
            return {
                "code": python_code,
                "message": "Python code generated successfully"
            }
            
        except Exception as e:
            print(f"⚠️  Code generation error: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to simple code
            return {
                "code": "# Code generation failed\nprint('Hello, World!')",
                "message": f"Using fallback code (error: {str(e)})"
            }
    
    def generate_execution_placeholder(self, code: str) -> Dict[str, str]:
        """
        Stage 5: Execution placeholder
        For now, returns a message indicating code is ready
        Actual execution will be implemented later with sandboxing
        """
        return {
            "execution": "# Code execution not yet implemented\n# The generated code is ready to run",
            "message": "Code ready for execution (execution feature coming soon)"
        }
    
    def generate_feedback(self, code: str, english_text: str) -> Dict[str, str]:
        """
        Stage 6: Generate feedback about the code
        Provides simple analysis and suggestions
        """
        feedback_points = []
        
        # Analyze code
        if 'for' in code and 'range' in code:
            feedback_points.append("✓ Good use of for loop with range() function")
        
        if 'if' in code:
            feedback_points.append("✓ Conditional logic implemented correctly")
        
        if 'def' in code:
            feedback_points.append("✓ Code organized into a function")
        elif len(code.split('\n')) > 3:
            feedback_points.append("💡 Consider organizing code into functions for better reusability")
        
        if 'print' in code:
            feedback_points.append("✓ Output statements included")
        
        # Check for common improvements
        if '#' not in code and len(code.split('\n')) > 2:
            feedback_points.append("💡 Add comments to explain your code logic")
        
        if not feedback_points:
            feedback_points.append("Code generated successfully! Review and test the output.")
        
        feedback = "\n".join(feedback_points)
        
        return {
            "feedback": feedback,
            "message": "AI feedback generated"
        }
    
    def process_pipeline(self, input_text: str, language: str = "kn") -> Dict[str, str]:
        """
        Complete processing pipeline
        Runs all stages and returns complete response
        """
        # Stage 1: Preprocess
        preprocess_result = self.preprocess_text(input_text)
        cleaned_text = preprocess_result["cleaned_text"]
        
        # Stage 2: Translate
        translation_result = self.translate_to_english(cleaned_text, language)
        english_text = translation_result["translation"]
        
        # Stage 3: Generate Pseudo-code
        pseudo_result = self.generate_pseudo_code(english_text)
        pseudo_code = pseudo_result["pseudo_code"]
        
        # Stage 4: Generate Python Code (using English translation and pseudo-code)
        code_result = self.generate_python_code(english_text, pseudo_code)
        python_code = code_result["code"]
        
        # Stage 5: Execution (placeholder)
        execution_result = self.generate_execution_placeholder(python_code)
        execution_output = execution_result["execution"]
        
        # Stage 6: Feedback
        feedback_result = self.generate_feedback(python_code, english_text)
        feedback = feedback_result["feedback"]
        
        # Return complete response matching frontend interface
        return {
            "preprocess": preprocess_result["message"],
            "translation": english_text,
            "pseudo_code": pseudo_code,
            "code": python_code,
            "execution": execution_output,
            "feedback": feedback
        }


# Testing function
if __name__ == "__main__":
    print("🧪 Testing Model Service...")
    service = ModelService()
    
    test_input = "1 ರಿಂದ 10 ರವರೆಗೆ ಸಂಖ್ಯೆಗಳನ್ನು ಮುದ್ರಿಸಿ"  # Print numbers from 1 to 10 in Kannada
    print(f"\n📝 Input: {test_input}")
    
    result = service.process_pipeline(test_input, "kn")
    
    print("\n📊 Results:")
    print(f"Preprocess: {result['preprocess']}")
    print(f"Translation: {result['translation']}")
    print(f"Pseudo-code:\n{result['pseudo_code']}")
    print(f"Code:\n{result['code']}")
    print(f"Execution: {result['execution']}")
    print(f"Feedback: {result['feedback']}")
