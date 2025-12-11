from fastapi import APIRouter, Depends
from sqlalchemy import text
from database import get_db
import os

router = APIRouter()

@router.get("/debug/db")
def debug_db(db = Depends(get_db)):
    """Check database connection and count"""
    try:
        # Check env var (masked)
        db_url = os.getenv("DATABASE_URL", "Not Set")
        masked_url = db_url
        if "postgresql" in db_url:
            parts = db_url.split("@")
            if len(parts) > 1:
                masked_url = f"postgresql://***@{parts[1]}"
        
        # Check DB connection
        result = db.execute(text("SELECT count(*) FROM colleges"))
        count = result.scalar()
        
        return {
            "status": "online",
            "database_url_configured": db_url != "Not Set",
            "database_url_masked": masked_url,
            "college_count": count,
            "message": "Connection successful"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "type": type(e).__name__
        }
