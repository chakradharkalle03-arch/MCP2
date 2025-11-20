"""
Test script for the Semiconductor Component Search API
Demonstrates the complete RAG flow
"""
import requests
import json
from pathlib import Path
import time

API_BASE = "http://localhost:8001"


def test_health():
    """Test health endpoint"""
    print("\n1. Testing health endpoint...")
    response = requests.get(f"{API_BASE}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")


def test_upload():
    """Test Excel upload"""
    print("\n2. Testing Excel upload...")
    excel_file = Path("examples/semiconductor_components.xlsx")
    
    if not excel_file.exists():
        print(f"   Error: {excel_file} not found!")
        print("   Run 'python create_example_excel.py' first")
        return False
    
    with open(excel_file, "rb") as f:
        files = {"file": (excel_file.name, f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        response = requests.post(f"{API_BASE}/upload", files=files)
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    return response.status_code == 200


def test_info():
    """Test collection info"""
    print("\n3. Testing collection info...")
    response = requests.get(f"{API_BASE}/info")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")


def test_question(question: str, n_results: int = 3):
    """Test question answering"""
    print(f"\n4. Testing question: '{question}'...")
    payload = {
        "question": question,
        "n_results": n_results
    }
    response = requests.post(
        f"{API_BASE}/ask",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Answer: {result.get('answer', 'N/A')[:200]}...")
    print(f"   Context retrieved: {len(result.get('context', []))} chunks")
    return result


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Testing Semiconductor Component Search API")
    print("="*60)
    
    try:
        # Test health
        test_health()
        
        # Test upload
        if test_upload():
            time.sleep(2)  # Wait for processing
            
            # Test info
            test_info()
            
            # Test questions
            questions = [
                "What MOSFET components are available?",
                "Show me voltage regulators",
                "What components work with 5V?",
                "List components from Texas Instruments"
            ]
            
            for q in questions:
                test_question(q)
                time.sleep(1)
        
        print("\n" + "="*60)
        print("Testing complete!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to API")
        print("Make sure the API server is running:")
        print("  python main.py")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()

