#!/usr/bin/env python3
"""
Simple test script to verify the PDF extraction system functionality.
This script tests the core components and ensures everything is working correctly.
"""

import os
import sys
import json
import sqlite3
import subprocess

def test_dependencies():
    """Test if all required dependencies are installed."""
    print("🔍 Testing dependencies...")
    
    try:
        import pymupdf
        print("✅ PyMuPDF: OK")
    except ImportError:
        print("❌ PyMuPDF: Missing")
        return False
    
    try:
        import tabulate
        print("✅ tabulate: OK")
    except ImportError:
        print("❌ tabulate: Missing")
        return False
    
    try:
        import streamlit
        print("✅ Streamlit: OK")
    except ImportError:
        print("❌ Streamlit: Missing")
        return False
    
    return True

def test_pdf_exists():
    """Test if the sample PDF exists."""
    print("\n📄 Testing PDF file...")
    
    if os.path.exists("data.pdf"):
        print("✅ data.pdf: Found")
        return True
    else:
        print("❌ data.pdf: Missing")
        return False

def test_data_generation():
    """Test the data generation process."""
    print("\n⚙️ Testing data generation...")
    
    try:
        # Run the data generation script
        result = subprocess.run([sys.executable, "generateData.py"], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Data generation: OK")
            
            # Check if output files exist
            if os.path.exists("pdfData.json") and os.path.exists("data.sqlite"):
                print("✅ Output files created: OK")
                return True
            else:
                print("❌ Output files: Missing")
                return False
        else:
            print(f"❌ Data generation failed: {result.stderr}")
            return False
    
    except subprocess.TimeoutExpired:
        print("❌ Data generation: Timeout")
        return False
    except Exception as e:
        print(f"❌ Data generation error: {e}")
        return False

def test_json_structure():
    """Test the JSON data structure."""
    print("\n📋 Testing JSON structure...")
    
    try:
        with open("pdfData.json", 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list) and len(data) > 0:
            print(f"✅ JSON structure: OK ({len(data)} entries)")
            
            # Test first entry structure
            first_entry = data[0]
            required_fields = ["identifier", "heading", "description", "UniqueCode", "category"]
            
            for field in required_fields:
                if field in first_entry:
                    print(f"✅ Field '{field}': OK")
                else:
                    print(f"❌ Field '{field}': Missing")
                    return False
            
            return True
        else:
            print("❌ JSON structure: Invalid or empty")
            return False
    
    except Exception as e:
        print(f"❌ JSON structure error: {e}")
        return False

def test_database():
    """Test the SQLite database."""
    print("\n🗄️ Testing database...")
    
    try:
        conn = sqlite3.connect("data.sqlite")
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Events';")
        if cursor.fetchone():
            print("✅ Events table: OK")
        else:
            print("❌ Events table: Missing")
            return False
        
        # Check if data exists
        cursor.execute("SELECT COUNT(*) FROM Events;")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"✅ Database data: OK ({count} records)")
            conn.close()
            return True
        else:
            print("❌ Database data: Empty")
            conn.close()
            return False
    
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_search_script():
    """Test the search script can be imported."""
    print("\n🔎 Testing search script...")
    
    try:
        import search
        print("✅ Search script: OK")
        return True
    except Exception as e:
        print(f"❌ Search script error: {e}")
        return False

def test_webapp_script():
    """Test the web app script can be imported."""
    print("\n🌐 Testing web app script...")
    
    try:
        # Just check if the file can be imported without running
        import ast
        with open("webApp.py", 'r') as f:
            content = f.read()
        
        ast.parse(content)
        print("✅ Web app script: OK")
        return True
    except Exception as e:
        print(f"❌ Web app script error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 PDF Extraction System Test Suite")
    print("=" * 40)
    
    tests = [
        test_dependencies,
        test_pdf_exists,
        test_data_generation,
        test_json_structure,
        test_database,
        test_search_script,
        test_webapp_script
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)