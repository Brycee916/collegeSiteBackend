"""
Update college data from College Scorecard API
Fetches accurate rankings, costs, and other data for all colleges
"""
import os
import requests
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

API_KEY = os.getenv('COLLEGE_SCORECARD_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./college_finder.db')
BASE_URL = 'https://api.data.gov/ed/collegescorecard/v1/schools'

def fetch_college_data(college_name, state=None):
    """Fetch college data from Scorecard API"""
    params = {
        'api_key': API_KEY,
        'school.name': college_name,
        'fields': 'id,school.name,school.city,school.state,school.zip,location.lat,location.lon,latest.admissions.admission_rate.overall,latest.cost.avg_net_price.overall,latest.completion.completion_rate_4yr_150nt,latest.admissions.sat_scores.average.overall,latest.admissions.act_scores.midpoint.cumulative,latest.student.size',
        '_per_page': 5
    }
    
    if state:
        params['school.state'] = state
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('results') and len(data['results']) > 0:
            return data['results'][0]  # Return best match
        return None
    except Exception as e:
        print(f"Error fetching data for {college_name}: {e}")
        return None

def update_college_from_api(conn, college_id, college_name, api_data):
    """Update college record with API data"""
    updates = []
    params = {'id': college_id}
    
    # Update location coordinates
    if api_data.get('location.lat') and api_data.get('location.lon'):
        updates.append("latitude = :latitude, longitude = :longitude")
        params['latitude'] = api_data['location.lat']
        params['longitude'] = api_data['location.lon']
    
    # Update admission rate
    if api_data.get('latest.admissions.admission_rate.overall'):
        updates.append("admission_rate = :admission_rate")
        params['admission_rate'] = api_data['latest.admissions.admission_rate.overall']
    
    # Update average cost
    if api_data.get('latest.cost.avg_net_price.overall'):
        updates.append("avg_cost = :avg_cost")
        params['avg_cost'] = int(api_data['latest.cost.avg_net_price.overall'])
    
    # Update graduation rate
    if api_data.get('latest.completion.completion_rate_4yr_150nt'):
        updates.append("graduation_rate = :graduation_rate")
        params['graduation_rate'] = api_data['latest.completion.completion_rate_4yr_150nt']
    
    # Update SAT scores
    if api_data.get('latest.admissions.sat_scores.average.overall'):
        updates.append("sat_score = :sat_score")
        params['sat_score'] = int(api_data['latest.admissions.sat_scores.average.overall'])
    
    # Update ACT scores  
    if api_data.get('latest.admissions.act_scores.midpoint.cumulative'):
        updates.append("act_score = :act_score")
        params['act_score'] = int(api_data['latest.admissions.act_scores.midpoint.cumulative'])
    
    if updates:
        sql = f"UPDATE colleges SET {', '.join(updates)} WHERE id = :id"
        conn.execute(text(sql), params)
        return [u.split('=')[0].strip() for u in updates]
    
    return []

def create_backup(conn):
    """Create backup of current college data"""
    backup_file = f"college_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    result = conn.execute(text("SELECT id, name, location, latitude, longitude, admission_rate, avg_cost, graduation_rate, sat_score, act_score FROM colleges"))
    
    backup_data = []
    for row in result:
        backup_data.append({
            'id': row[0],
            'name': row[1],
            'location': row[2],
            'latitude': float(row[3]) if row[3] else None,
            'longitude': float(row[4]) if row[4] else None,
            'admission_rate': float(row[5]) if row[5] else None,
            'avg_cost': row[6],
            'graduation_rate': float(row[7]) if row[7] else None,
            'sat_score': row[8],
            'act_score': row[9]
        })
    
    with open(backup_file, 'w') as f:
        json.dump(backup_data, f, indent=2)
    
    print(f"✅ Backup created: {backup_file}")
    return backup_file

def update_colleges(limit=None, test_mode=True):
    """Update college data from API"""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Create backup first
        if not test_mode:
            create_backup(conn)
        
        # Get colleges to update
        sql = "SELECT id, name, location FROM colleges"
        if limit:
            sql += f" LIMIT {limit}"
        
        result = conn.execute(text(sql))
        colleges = result.fetchall()
        total = len(colleges)
        
        print(f"\n{'='*60}")
        print(f"{'TEST MODE' if test_mode else 'FULL UPDATE'}: Updating {total} colleges")
        print(f"{'='*60}\n")
        
        updated_count = 0
        failed_count = 0
        
        for idx, (college_id, college_name, location) in enumerate(colleges, 1):
            print(f"[{idx}/{total}] Processing: {college_name}")
            
            # Extract state from location if possible
            state = None
            if location and ',' in location:
                state = location.split(',')[-1].strip()
            
            # Fetch data from API
            api_data = fetch_college_data(college_name, state)
            
            if api_data:
                updated_fields = update_college_from_api(conn, college_id, college_name, api_data)
                
                if updated_fields:
                    conn.commit()
                    updated_count += 1
                    print(f"  ✅ Updated: {', '.join(updated_fields)}")
                else:
                    print(f"  ⚠️  No new data available")
            else:
                failed_count += 1
                print(f"  ❌ Not found in API")
            
            # Rate limiting: 1000 requests/hour = ~1 per 4 seconds
            if idx < total:
                time.sleep(4)
        
        print(f"\n{'='*60}")
        print(f"Summary:")
        print(f"  Total processed: {total}")
        print(f"  Successfully updated: {updated_count}")
        print(f"  Failed/Not found: {failed_count}")
        print(f"{'='*60}\n")

def seed_database(limit=100):
    """Seed database with initial colleges"""
    print(f"\nExample: Seeding database with {limit} colleges...")
    engine = create_engine(DATABASE_URL)
    
    params = {
        'api_key': API_KEY,
        'fields': 'id,school.name,school.city,school.state',
        '_per_page': 100,
        '_sort': 'latest.student.size:desc' # Get largest schools first
    }
    
    with engine.connect() as conn:
        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            count = 0
            for item in data.get('results', []):
                if count >= limit: break
                
                name = item.get('school.name')
                city = item.get('school.city')
                state = item.get('school.state')
                location = f"{city}, {state}" if city and state else city
                
                # Check if exists
                exists = conn.execute(text("SELECT id FROM colleges WHERE name = :name"), {'name': name}).fetchone()
                
                if not exists:
                    conn.execute(text("INSERT INTO colleges (name, location) VALUES (:name, :location)"), 
                               {'name': name, 'location': location})
                    print(f"  + Added: {name}")
                    count += 1
                else:
                    print(f"  . Skpping (exists): {name}")
            
            conn.commit()
            print(f"✅ Seeding complete. Added {count} colleges.")
            
        except Exception as e:
            print(f"❌ Seeding failed: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--seed':
            seed_database(limit=100)
        elif sys.argv[1] == '--full':
            print("⚠️  FULL UPDATE MODE - This will update ALL colleges!")
            confirm = input("Type 'yes' to confirm: ")
            if confirm.lower() == 'yes':
                update_colleges(limit=None, test_mode=False)
            else:
                print("Cancelled.")
    else:
        print("Running in TEST MODE (50 colleges)")
        print("Use --full flag for full update")
        print("Use --seed flag to populate empty database")
        update_colleges(limit=50, test_mode=True)
