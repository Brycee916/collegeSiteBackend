import requests

urls = [
    "https://ed-public-download.app.cloud.gov/nces-data/Most-Recent-Cohorts-All-Data-Elements.csv",
    "https://ed-public-download.app.cloud.gov/nces-data/Most-Recent-Cohorts-All-Data-Elements.zip",
    "https://ed-public-download.app.cloud.gov/nces-data/Most-Recent-Cohorts-Scorecard-Elements.zip"
]

for url in urls:
    print(f"Checking {url}...")
    try:
        r = requests.head(url, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print(f"Content-Length: {r.headers.get('content-length')}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)
