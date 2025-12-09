from backend import database, models, auth
from sqlalchemy.orm import Session

def create_user():
    db = database.SessionLocal()
    email = "test@example.com"
    password = "password123"
    
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        print(f"User {email} already exists. Updating password...")
        existing.hashed_password = auth.get_password_hash(password)
        # Ensure premium for testing features if needed, or leave as is
        existing.is_premium = True 
    else:
        print(f"Creating user {email}...")
        user = models.User(
            email=email,
            hashed_password=auth.get_password_hash(password),
            is_premium=True
        )
        db.add(user)
    
    db.commit()
    print("User setup complete.")
    db.close()

if __name__ == "__main__":
    create_user()
