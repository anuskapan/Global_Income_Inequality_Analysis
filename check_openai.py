import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

print("🔍 Checking OpenAI Configuration...")
print("=" * 60)

try:
    # Get available models
    models = openai.models.list()
    
    print("✅ API Key is valid!\n")
    print("📋 Available Models:")
    print("-" * 60)
    
    # Filter for GPT models
    gpt_models = []
    for model in models.data:
        if 'gpt' in model.id.lower():
            gpt_models.append(model.id)
    
    # Sort and display
    gpt_models.sort(reverse=True)
    
    recommended = []
    for model in gpt_models:
        icon = ""
        if 'gpt-4' in model:
            icon = "🌟"
            recommended.append(model)
        elif 'gpt-3.5' in model:
            icon = "✅"
            if not recommended:  # If no GPT-4, recommend GPT-3.5
                recommended.append(model)
        
        print(f"{icon} {model}")
    
    print("-" * 60)
    print("\n💡 Recommended Models:")
    for model in recommended[:3]:
        print(f"   • {model}")
    
    print("\n🎯 Best Choice:")
    if any('gpt-4' in m for m in recommended):
        best = [m for m in recommended if 'gpt-4' in m][0]
        print(f"   {best} (Most capable)")
    else:
        print(f"   gpt-3.5-turbo (Fast and reliable)")
    
except openai.AuthenticationError:
    print("❌ Authentication Error!")
    print("   Your API key is invalid or expired.")
    print("   Get a new key: https://platform.openai.com/api-keys")

except Exception as e:
    print(f"❌ Error: {e}")

print("=" * 60)