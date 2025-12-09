import requests
import json
import time

# API Configuration
API_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"
API_KEY = "DEMO_KEY"
OUTPUT_FILE = "backend/colleges_real.json"

FIELDS = [
    "id",
    "school.name",
    "school.city",
    "school.state",
    "school.school_url",
    "school.locale",
    "latest.student.size",
    "latest.admissions.sat_scores.average.overall",
    "latest.admissions.act_scores.midpoint.cumulative",
    "latest.completion.completion_rate_4yr_150nt", # One of the grad rate fields
    "latest.cost.attendance.academic_year",
    "location.lat",
    "location.lon",
    "latest.admissions.admission_rate.overall"
]

def fetch_and_process_data():
    print("Fetching data from College Scorecard API...")
    
    colleges = []
    page = 0
    per_page = 100
    total_pages = 25 # Limit to ~2500 colleges to respect demo key and time
    
    while True:
        print(f"Fetching page {page + 1}/{total_pages if isinstance(total_pages, int) else '?'}...")
        try:
            params = {
                "api_key": API_KEY,
                "per_page": per_page,
                "page": page,
                "fields": ",".join(FIELDS),
                "school.degrees_awarded.highest__range": "3..4", # Bachelor's+
                "latest.student.size__range": "100..", # Lower limit to include smaller valid colleges
                "sort": "latest.student.size:desc"
            }
            
            response = requests.get(API_URL, params=params, timeout=15)
            
            if response.status_code == 429:
                print("Rate limit hit. Sleeping for 10 seconds...")
                time.sleep(10)
                continue
                
            response.raise_for_status()
            data = response.json()
            
            # Update total pages on first request if possible, though API structure might not give it clearly in metadata always
            if 'metadata' in data and 'total' in data['metadata']:
                total_records = data['metadata']['total']
                total_pages = (total_records // per_page) + 1
                
            results = data.get('results', [])
            if not results:
                print("No more results.")
                break
                
            for item in results:
                # Extract and Map fields
                name = item.get("school.name")
                if not name: continue
                
                url = item.get("school.school_url")
                if url and not url.startswith("http"):
                    url = "http://" + url
                
                # Locale mapping
                locale = item.get("school.locale")
                campus_setting = "Suburban"
                if locale:
                    l_str = str(locale)
                    if l_str.startswith('1'): campus_setting = "Urban"
                    elif l_str.startswith('2'): campus_setting = "Suburban"
                    elif l_str.startswith('3'): campus_setting = "Town"
                    elif l_str.startswith('4'): campus_setting = "Rural"

                college = {
                    "name": name,
                    "location": f"{item.get('school.city')}, {item.get('school.state')}",
                    "website_url": url,
                    "enrollment": item.get("latest.student.size") or 0,
                    "sat_score": item.get("latest.admissions.sat_scores.average.overall"),
                    "act_score": item.get("latest.admissions.act_scores.midpoint.cumulative"),
                    "graduation_rate": item.get("latest.completion.completion_rate_4yr_150nt"),
                    "avg_cost": item.get("latest.cost.attendance.academic_year"),
                    "campus_setting": campus_setting,
                    "latitude": item.get("location.lat"),
                    "longitude": item.get("location.lon"),
                    "admission_rate": item.get("latest.admissions.admission_rate.overall"),
                    "ranking": 9999
                }
                
                colleges.append(college)
            
            page += 1
            # Simple progress
            print(f"Fetched {len(results)} schools. Total so far: {len(colleges)}")
            
            # Be nice to the API
            time.sleep(0.3)
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
            # Retry a few times? For now just break to save what we have or continue
            # If it's a connectivity issue, maybe retry
            time.sleep(5)
            continue

    print(f"Fetched {len(colleges)} colleges. Post-processing...")
    
    # Simple ranking generation
    for i, c in enumerate(colleges):
        c['ranking'] = i + 1
        # Fill missing stats with reasonable defaults or keep None (Frontend handles it?)
        # Let's clean up None values for display
        if c['enrollment'] is None: c['enrollment'] = 0
        
    print(f"Saving to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(colleges, f, indent=2)
        
    print("Done!")

if __name__ == "__main__":
    fetch_and_process_data()
