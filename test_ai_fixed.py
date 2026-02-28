from utils.ai_service import AIInsightEngine
import pandas as pd

print("🤖 Testing AI Service...")
print("=" * 60)

try:
    # Initialize AI engine
    ai = AIInsightEngine()
    print(f"✅ AI Engine initialized with model: {ai.model}\n")
    
    # Load data
    print("📊 Loading data...")
    df = pd.read_excel(r"C:\Users\Yashu\OneDrive\Desktop\infy\WIID_Cleaned_Imputed_Renamed.xlsx")
    print(f"✅ Loaded {len(df)} records\n")
    
    # Test 1: Simple question
    print("📝 Test 1: Asking a simple question...")
    print("-" * 60)
    response = ai.answer_question(df, "What is income inequality?")
    print(response)
    print("\n")
    
    # Test 2: Country analysis
    print("📝 Test 2: Analyzing United States...")
    print("-" * 60)
    response = ai.analyze_country(df, "United States")
    print(response)
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()