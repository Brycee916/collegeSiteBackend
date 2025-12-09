import requests
import json

BASE_URL = "http://localhost:8000"

def verify_career_search():
    print("Verifying Career Advisor API...")
    
    # Test Cases
    queries = ["Doctor", "software engineer", "NURSE", "Business Analyst"]
    
    for q in queries:
        print(f"\nSearching for '{q}'...")
        r = requests.get(f"{BASE_URL}/careers/search?q={q}")
        
        if r.status_code != 200:
            print(f"❌ Failed to fetch. Status: {r.status_code}")
            continue
            
        data = r.json()
        
        if not data.get('found'):
            print(f"❌ Career not found in mock DB.")
            continue
            
        print(f"✅ Found Career: {data['career']['title']}")
        print(f"   Degree Focus: {data['career']['degree_focus']}")
        print(f"   Roadmap Steps: {len(data['career']['steps'])}")
        
        colleges = data.get('recommended_colleges', [])
        print(f"   Recommended Colleges: {len(colleges)}")
        
        if len(colleges) > 0:
            print(f"   Sample: {colleges[0]['name']}")
            
    print("\nVerification Complete.")

if __name__ == "__main__":
    verify_career_search()
