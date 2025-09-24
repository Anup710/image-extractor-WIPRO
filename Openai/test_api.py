#!/usr/bin/env python3
"""
Quick test script to verify API connectivity
"""
import requests
import time

def test_backend():
    print("Testing Columbus CV Backend API...")

    # Test health endpoint
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']} at {data['timestamp']}")
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running. Please start the backend server first.")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Columbus CV Analyzer - API Test")
    print("=" * 40)

    if test_backend():
        print("\n✅ Backend is ready!")
        print("\nTo test the full application:")
        print("1. Start backend: cd backend && python main.py")
        print("2. Start frontend: cd frontend && npm run dev")
        print("3. Open: http://localhost:5173")
    else:
        print("\n❌ Please start the backend first:")
        print("cd backend && python main.py")