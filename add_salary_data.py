from backend import database, models

db = database.SessionLocal()

# Check existing salary data
existing = db.query(models.SalaryData).all()
print(f"Existing salary records: {len(existing)}")

# Add sample salary data for college 1 (MIT) if none exists
if len(existing) == 0:
    print("Adding sample salary data...")
    
    # Get MIT's degrees
    mit = db.query(models.College).filter(models.College.id == 1).first()
    if mit and mit.degrees:
        for degree in mit.degrees[:3]:  # Add for first 3 degrees
            salary = models.SalaryData(
                college_id=1,
                degree_id=degree.id,
                median_salary_1yr=75000 + (degree.id * 5000),
                median_salary_5yr=110000 + (degree.id * 8000)
            )
            db.add(salary)
        db.commit()
        print(f"Added salary data for {len(mit.degrees[:3])} degrees")
    else:
        print("MIT not found or has no degrees")
else:
    print("Salary data already exists")

db.close()
