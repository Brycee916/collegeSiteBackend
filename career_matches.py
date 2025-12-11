from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas, database, auth

router = APIRouter()

@router.post("/career-matches")
def save_career_matches(
    matches: List[dict],
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Save user's career match results from questionnaire"""
    # Delete existing matches for this user
    db.query(models.CareerMatch).filter(models.CareerMatch.user_id == current_user.id).delete()
    
    # Save new matches
    for match in matches:
        career_match = models.CareerMatch(
            user_id=current_user.id,
            career_title=match['title'],
            match_score=match['score'],
            created_at=datetime.utcnow().isoformat()
        )
        db.add(career_match)
    
    db.commit()
    return {"message": f"Saved {len(matches)} career matches"}

@router.get("/career-matches")
def get_career_matches(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Get user's saved career matches"""
    matches = db.query(models.CareerMatch).filter(
        models.CareerMatch.user_id == current_user.id
    ).order_by(models.CareerMatch.match_score.desc()).all()
    
    return [
        {
            "id": m.id,
            "career_title": m.career_title,
            "match_score": m.match_score,
            "created_at": m.created_at
        }
        for m in matches
    ]
