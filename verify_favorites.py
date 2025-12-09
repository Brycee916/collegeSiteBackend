import requests

BASE_URL = "http://localhost:8000"
USER_EMAIL = "favtest@example.com"
USER_PASS = "password123"

def verify_favorites():
    print("Verifying Favorites API...")
    
    # 1. Register/Login
    session = requests.Session()
    
    print("Attempting registration...")
    r = session.post(f"{BASE_URL}/users/", json={"email": USER_EMAIL, "password": USER_PASS})
    print(f"Registration status: {r.status_code}")

    print("Logging in...")
    login_data = {"username": USER_EMAIL, "password": USER_PASS}
    r = session.post(f"{BASE_URL}/token", data=login_data)
    
    if r.status_code != 200:
        print(f"Login failed: {r.text}")
        return
        
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print("Logged in successfully.")
    
    # 2. Get a college ID
    print("Fetching a college...")
    r = session.get(f"{BASE_URL}/colleges/?limit=1")
    colleges = r.json()
    if not colleges:
        print("No colleges found!")
        return
    
    college_id = colleges[0]['id']
    print(f"Target College ID: {college_id}")
    
    # 3. Add to Favorites
    print(f"Adding college {college_id} to favorites...")
    r = session.post(f"{BASE_URL}/colleges/{college_id}/favorite", headers=headers)
    print(f"Add response: {r.status_code} {r.json()}")
    if r.status_code != 200:
        print("Failed to add favorite")
        return

    # 4. List Favorites
    print("Listing favorites...")
    r = session.get(f"{BASE_URL}/favorites/", headers=headers)
    favs = r.json()
    print(f"Favorites count: {len(favs)}")
    
    found = any(c['id'] == college_id for c in favs)
    if found:
        print("✅ College found in favorites list.")
    else:
        print("❌ College NOT found in favorites list.")
        
    # 5. Remove Favorite
    print("Removing favorite...")
    r = session.delete(f"{BASE_URL}/colleges/{college_id}/favorite", headers=headers)
    print(f"Remove response: {r.status_code} {r.json()}")
    
    # 6. Verify Removal
    r = session.get(f"{BASE_URL}/favorites/", headers=headers)
    favs = r.json()
    found = any(c['id'] == college_id for c in favs)
    if not found:
        print("✅ College successfully removed.")
    else:
        print("❌ College still in favorites list.")

if __name__ == "__main__":
    verify_favorites()
