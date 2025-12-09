from backend.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

try:
    # Add column if it doesn't exist
    db.execute(text("ALTER TABLE colleges ADD COLUMN logo_url TEXT"))
    db.commit()
    print("Column 'logo_url' added successfully!")
except Exception as e:
    if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
        print("Column 'logo_url' already exists, skipping...")
    else:
        print(f"Error: {e}")
    db.rollback()

db.close()
