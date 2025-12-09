import requests
import json
import csv
import io

# List of potential datasets (JSON or CSV)
urls = [
    # 18F (Government Tech) - often has clean data
    {"url": "https://raw.githubusercontent.com/18F/api-data-bootcamp/master/data/colleges.csv", "type": "csv_18f"},
    # SimonW Gist (Likely has coords)
    {"url": "https://gist.githubusercontent.com/simonw/1a60e0a7e584d4b85c13/raw/us-colleges.csv", "type": "csv_simonw"},
    # OpenDataSoft (Direct Export URL - verified pattern)
    {"url": "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/us-colleges-and-universities/exports/csv?lang=en&timezone=America%2FNew_York&use_labels=true&delimiter=%3B", "type": "csv_ods"},
    # Ryan Serpico (Retry with different path? No, we know 404)
    # Fallback: Just verified dataset?
]

def download_file():
    print("Attempting to download US College data with Coordinates...")
    
    for entry in urls:
        url = entry["url"]
        try:
            print(f"Checking {url}...")
            r = requests.get(url)
            if r.status_code == 200:
                print(f"✅ Success! Downloading {entry['type']}...")
                
                # Save Raw
                with open("backend/mass_data_raw.txt", "wb") as f:
                    f.write(r.content)
                
                # Verify Content (Check for "lat" or "latitude")
                content_sample = r.text[:1000].lower()
                if "lat" in content_sample or "coord" in content_sample:
                    print("✅ Verified: Contains latitude/coordinates info.")
                    if entry['type'] == 'json':
                        with open("backend/us_colleges_mass.json", "wb") as f:
                            f.write(r.content)
                    else:
                         # Rename accordingly if CSV
                        with open("backend/us_colleges_mass.csv", "wb") as f:
                            f.write(r.content)
                    return True
                else:
                    print("⚠️ Warning: Data downloaded but might missing coordinates. Skipping to next candidate.")
            else:
                print(f"❌ Failed: {r.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    print("❌ All downloads failed.")
    return False

if __name__ == "__main__":
    download_file()
