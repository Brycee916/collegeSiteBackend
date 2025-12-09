
import requests
import json

try:
    response = requests.get("http://localhost:8000/colleges/1")
    data = response.json()
    print("College Name:", data.get('name'))
    print("Degrees Count:", len(data.get('degrees', [])))
    print("First Degree:", data.get('degrees')[0] if data.get('degrees') else "None")
    print("Full Degrees:", json.dumps(data.get('degrees', []), indent=2))
except Exception as e:
    print(e)
