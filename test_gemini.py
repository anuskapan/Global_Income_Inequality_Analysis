import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Testing Gemini Setup...")
print("=" * 60)

# Test 1: Check API key
api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    print(f"✅ GEMINI_API_KEY found: {api_key[:15]}...")
else:
    print("❌ GEMINI_API_KEY not found in .env")
    exit()

# Test 2: List available models
print("\n📋 Checking available Gemini models...")
try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    
    models = genai.list_models()
    print("\n✅ Available models that support generateContent:")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"   • {model.name}")
    
except Exception as e:
    print(f"❌ Error listing models: {e}")
    exit()

# Test 3: Initialize AI Engine
print("\n🤖 Initializing AI Engine...")
try:
    from utils.ai_service_gemini import AIInsightEngine
    ai = AIInsightEngine()
    print("✅ AI Engine initialized successfully!")
except Exception as e:
    print(f"❌ Initialization failed: {e}")
    import traceback
    traceback.print_exc()
    exit()

# Test 4: Simple test
print("\n🧪 Testing AI response...")
print("-" * 60)
try:
    import pandas as pd
    df = pd.read_excel(r"C:\Users\Yashu\OneDrive\Desktop\infy\data\WIID_Cleaned_Imputed_Renamed.xlsx")
    
    response = ai.answer_question(df, "What is the Gini Index in 2 sentences?")
    print(response)
    print("-" * 60)
    print("\n✅ ALL TESTS PASSED! 🎉")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()