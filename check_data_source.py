import requests

urls = [
    "https://raw.githubusercontent.com/ryan-serpico/us-college-coordinates/main/output/us-college-coordinates.json",
    "https://raw.githubusercontent.com/ryan-serpico/us-college-coordinates/master/output/us-college-coordinates.json",
    "https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json"
]

print("Checking URLs...")
for url in urls:
    try:
        r = requests.head(url)
        print(f"{url}: {r.status_code}")
        if r.status_code == 200:
            print(f"FOUND VALID URL: {url}")
            # Download it immediately
            print("Downloading...")
            r_get = requests.get(url)
            with open("backend/us_colleges_raw.json", "wb") as f:
                f.write(r_get.content)
            print("Downloaded to backend/us_colleges_raw.json")
            break
    except Exception as e:
        print(f"Error checking {url}: {e}")
