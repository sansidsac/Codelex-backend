"""
Quick test script for the updated model service
"""

from model_service import ModelService

def test_code_generation():
    print("🧪 Testing Updated Model Service...")
    print("="*60)
    
    service = ModelService()
    
    # Test case 1: Simple loop
    test_input_1 = "1 ರಿಂದ 10 ರವರೆಗೆ ಸಂಖ್ಯೆಗಳನ್ನು ಮುದ್ರಿಸಿ"
    print(f"\n📝 Test 1: {test_input_1}")
    print("-"*60)
    
    result_1 = service.process_pipeline(test_input_1, "kn")
    
    print(f"✅ Translation: {result_1['translation']}")
    print(f"\n✅ Pseudo-code:\n{result_1['pseudo_code']}")
    print(f"\n✅ Python Code:\n{result_1['code']}")
    print(f"\n✅ Feedback: {result_1['feedback']}")
    
    # Test case 2: Even numbers
    test_input_2 = "1 ರಿಂದ 20 ರವರೆಗೆ ಸಮ ಸಂಖ್ಯೆಗಳನ್ನು ಮುದ್ರಿಸಿ"
    print(f"\n\n📝 Test 2: {test_input_2}")
    print("-"*60)
    
    result_2 = service.process_pipeline(test_input_2, "kn")
    
    print(f"✅ Translation: {result_2['translation']}")
    print(f"\n✅ Python Code:\n{result_2['code']}")
    
    # Test case 3: Sum
    test_input_3 = "1 ರಿಂದ 100 ರವರೆಗೆ ಸಂಖ್ಯೆಗಳ ಮೊತ್ತವನ್ನು ಲೆಕ್ಕ ಮಾಡಿ"
    print(f"\n\n📝 Test 3: {test_input_3}")
    print("-"*60)
    
    result_3 = service.process_pipeline(test_input_3, "kn")
    
    print(f"✅ Translation: {result_3['translation']}")
    print(f"\n✅ Python Code:\n{result_3['code']}")
    
    print("\n" + "="*60)
    print("🎉 All tests completed!")

if __name__ == "__main__":
    test_code_generation()
