from backend import database, models

db = database.SessionLocal()

# Function to generate logo URL from college name
def get_logo_url(college_name):
    # Extract initials from college name
    words = college_name.split()
    initials = ''.join([w[0] for w in words if w[0].isupper()])[:3]
    # Use UI Avatars service with college colors
    return f"https://ui-avatars.com/api/?name={initials}&size=200&background=1e40af&color=fff&bold=true&format=svg"

# Update all colleges with logo URLs
colleges = db.query(models.College).all()
print(f"Updating {len(colleges)} colleges with logo URLs...")

for college in colleges:
    college.logo_url = get_logo_url(college.name)
    
db.commit()
print("Logo URLs added successfully!")
db.close()
