from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# The URL provided by the user
REMOTE_URL = "postgresql://postgres:CollegeFinderProject@db.gkhhwypbeplphzpdikbv.supabase.co:5432/postgres"

def check_remote_db():
    print(f"Connecting to: {REMOTE_URL.split('@')[1]}...") # Mask password
    try:
        engine = create_engine(REMOTE_URL)
        with engine.connect() as conn:
            # Check table existence
            result = conn.execute(text("SELECT count(*) FROM colleges"))
            count = result.scalar()
            print(f"✅ Connection successful!")
            print(f"📊 College Count: {count}")
            
            if count == 0:
                print("⚠️  Database is empty!")
            else:
                print("🎉 Database has data!")

            # Check a sample
            result = conn.execute(text("SELECT name FROM colleges LIMIT 3"))
            print("\nSample Colleges:")
            for row in result:
                print(f" - {row[0]}")

    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    check_remote_db()
