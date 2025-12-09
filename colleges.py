from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
from . import models, schemas, database, auth

router = APIRouter()

@router.get("/colleges/", response_model=List[schemas.College])
def get_colleges(
    skip: int = 0, 
    limit: int = 20, 
    search: Optional[str] = None,
    degree_type: Optional[str] = None,
    state: Optional[str] = None,
    max_cost: Optional[int] = None,
    max_admission_rate: Optional[float] = None,
    sort_by: Optional[str] = "ranking", # ranking, cost_asc, cost_desc
    db: Session = Depends(database.get_db)
):
    query = db.query(models.College).options(joinedload(models.College.degrees))

    if search:
        # Note: If filtering by degree, join is already needed, but good to be explicit for response
        if not degree_type:
             query = query.outerjoin(models.College.degrees)
        query = query.filter(
            or_(
                models.College.name.ilike(f"%{search}%"),
                models.Degree.name.ilike(f"%{search}%")
            )
        ).distinct()
    
    if degree_type:
        query = query.join(models.College.degrees).filter(models.Degree.type == degree_type)
        
    if state:
        # Strict lookup: check for comma + space + state (e.g. ", CA")
        query = query.filter(models.College.location.like(f"%, {state}"))

    if max_cost:
        query = query.filter(models.College.avg_cost <= max_cost)
        
    if max_admission_rate:
         query = query.filter(models.College.admission_rate <= max_admission_rate)

    if sort_by == "ranking" or sort_by == "ranking_asc":
        query = query.order_by(models.College.ranking.asc())
    elif sort_by == "ranking_desc":
        query = query.order_by(models.College.ranking.desc())

    colleges = query.offset(skip).limit(limit).all()
    return colleges

@router.get("/colleges/{college_id}", response_model=schemas.College)
def get_college_details(college_id: int, db: Session = Depends(database.get_db)):
    college = db.query(models.College).options(joinedload(models.College.degrees)).filter(models.College.id == college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    return college


@router.get("/colleges/{college_id}/salary", response_model=List[schemas.SalaryData])
def get_college_salary_data(
    college_id: int, 
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Get salary data for a college - available to all logged-in users"""
    salary_data = db.query(models.SalaryData).filter(models.SalaryData.college_id == college_id).all()
    return salary_data

# Favorites Endpoints

@router.post("/colleges/{college_id}/favorite")
def add_favorite(
    college_id: int, 
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    college = db.query(models.College).filter(models.College.id == college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    
    if college in current_user.favorites:
        return {"message": "Already favorited"}
        
    current_user.favorites.append(college)
    db.commit()
    return {"message": "Added to favorites"}

@router.delete("/colleges/{college_id}/favorite")
def remove_favorite(
    college_id: int, 
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    college = db.query(models.College).filter(models.College.id == college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
        
    if college in current_user.favorites:
        current_user.favorites.remove(college)
        db.commit()
        return {"message": "Removed from favorites"}
    
    return {"message": "Not in favorites"}

@router.get("/favorites/", response_model=List[schemas.College])
def get_favorites(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    return current_user.favorites
