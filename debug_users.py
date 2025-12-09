from backend import database, models
from sqlalchemy.orm import Session

db = database.SessionLocal()
users = db.query(models.User).all()
print(f"Found {len(users)} users:")
for u in users:
    print(f"ID: {u.id}, Email: {u.email}, Premium: {u.is_premium}")
db.close()
