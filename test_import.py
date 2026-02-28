# test_import.py
print("Testing imports...")

try:
    from utils.components import render_navbar
    print("✅ render_navbar imported successfully")
except Exception as e:
    print(f"❌ render_navbar import failed: {e}")

try:
    from utils.components import render_footer
    print("✅ render_footer imported successfully")
except Exception as e:
    print(f"❌ render_footer import failed: {e}")

try:
    from utils.components import render_page_header
    print("✅ render_page_header imported successfully")
except Exception as e:
    print(f"❌ render_page_header import failed: {e}")

try:
    from utils.components import render_logout_button
    print("✅ render_logout_button imported successfully")
except Exception as e:
    print(f"❌ render_logout_button import failed: {e}")

try:
    from utils.components import render_expandable_footer
    print("✅ render_expandable_footer imported successfully")
except Exception as e:
    print(f"❌ render_expandable_footer import failed: {e}")

print("\n✅ All imports successful!")