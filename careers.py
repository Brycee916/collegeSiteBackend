from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter()

# Data: Career Roadmaps
# Logic: Map a "Dream Job" to a standard Degree and a list of actionable steps.
CAREER_ROADMAPS = {
    "software engineer": {
        "title": "Software Engineer",
        "degree_focus": "Computer Science",
        "description": "Design, develop, and maintain software systems.",
        "steps": [
            "Earn a Bachelor's Degree in Computer Science or Software Engineering.",
            "Build a portfolio of personal projects (Web Apps, Mobile Apps).",
            "Complete an internship to gain industry experience.",
            "Practice coding interviews (Data Structures & Algorithms)."
        ],
        "outlook": "Growing much faster than average (22% growth)"
    },
    "doctor": {
        "title": "Medical Doctor (Physician)",
        "degree_focus": "Biology", # Simplification for linking to Pre-med majors like Biology
        "description": "Diagnose and treat injuries or illnesses.",
        "steps": [
            "Earn a Bachelor's Degree (commonly Biology, Chemistry, or Pre-Med).",
            "Take the MCAT (Medical College Admission Test).",
            "Attend Medical School (4 years).",
            "Complete a Residency program (3-7 years)."
        ],
        "outlook": "Growing faster than average (3% growth)"
    },
    "nurse": {
        "title": "Registered Nurse",
        "degree_focus": "Nursing",
        "description": "Provide and coordinate patient care and educate patients.",
        "steps": [
            "Earn a Bachelor's of Science in Nursing (BSN).",
            "Pass the NCLEX-RN exam.",
            "Obtain state licensure.",
            "Gain clinical experience."
        ],
        "outlook": "Growing faster than average (6% growth)"
    },
    "business analyst": {
        "title": "Business Analyst",
        "degree_focus": "Business Administration",
        "description": "Analyze an organization or business domain to document processes or systems.",
        "steps": [
            "Earn a Bachelor's Degree in Business Administration or Economics.",
            "Develop SQL and data visualization skills.",
            "Gain experience in project management.",
            "Consider certification (CBAP)."
        ],
        "outlook": "Growing faster than average (11% growth)"
    },
    "data scientist": {
        "title": "Data Scientist",
        "degree_focus": "Data Science",
        "description": "Extract insights from data using scientific methods, processes, and algorithms.",
        "steps": [
            "Earn a Bachelor's in Data Science, CS, or Math.",
            "Master Python, R, and SQL.",
            "Build predictive models and visualization dashboards.",
            "Consider a Master's degree for advanced roles."
        ],
        "outlook": "Growing much faster than average (35% growth)"
    },
    "lawyer": {
        "title": "Lawyer",
        "degree_focus": "Political Science", # Pre-law path
        "description": "Advise and represent individuals, businesses, and government agencies on legal issues.",
        "steps": [
            "Earn a Bachelor's Degree (Political Science, History, or English).",
            "Take the LSAT (Law School Admission Test).",
            "Earn a Juris Doctor (J.D.) degree.",
            "Pass the Bar Exam."
        ],
        "outlook": "Growing as fast as average (8% growth)"
    }
}

@router.get("/careers/search")
def search_careers(q: str, db: Session = Depends(database.get_db)):
    query = q.lower().strip()
    
    # Simple keyword match
    matched_key = None
    for key in CAREER_ROADMAPS:
        if query in key or key in query:
            matched_key = key
            break
    
    if not matched_key:
        return {"found": False, "message": "No specific path found for this career yet. Try 'Engineer', 'Doctor', 'Nurse', etc."}
    
    career_info = CAREER_ROADMAPS[matched_key]
    
    # Find colleges that offer the recommended degree
    # We join College -> Degree
    target_degree = career_info["degree_focus"]
    
    # Note: In our simple schema, we check if the college links to a Degree with this name.
    # We'll use a fuzzy match on degree name or exact.
    
    colleges = db.query(models.College).join(models.College.degrees).filter(
        models.Degree.name.ilike(f"%{target_degree}%")
    ).limit(6).all()
    
    return {
        "found": True,
        "career": career_info,
        "recommended_colleges": colleges
    }
