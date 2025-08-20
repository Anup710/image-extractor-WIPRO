# test_file_access.py
import os
import sys

def test_file_access():
    print("Current working directory:", os.getcwd())
    print("\n" + "="*50)
    
    # Test different path variations
    test_paths = [
        "../images/",
        "images/",
        "./images/",
        "Images/",  # Case sensitivity check
    ]
    
    for path in test_paths:
        print(f"Testing path: {path}")
        if os.path.exists(path):
            print(f"  ✅ Directory exists!")
            try:
                files = os.listdir(path)
                pdf_files = [f for f in files if f.lower().endswith('.pdf')]
                print(f"  📁 Found {len(files)} total files")
                print(f"  📄 Found {len(pdf_files)} PDF files")
                if pdf_files:
                    print(f"  PDF files: {pdf_files[:3]}{'...' if len(pdf_files) > 3 else ''}")
            except PermissionError:
                print(f"  ❌ Permission denied")
        else:
            print(f"  ❌ Directory does not exist")
        print()

if __name__ == "__main__":
    test_file_access()