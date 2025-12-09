from typing import List, Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_premium: bool

    class Config:
        from_attributes = True


class DegreeBase(BaseModel):
    name: str
    type: str

class Degree(DegreeBase):
    id: int

    class Config:
        from_attributes = True

class CollegeBase(BaseModel):
    name: str
    location: str
    admission_rate: float
    avg_cost: int
    ranking: int
    website_url: Optional[str] = None
    image_url: Optional[str] = None
    logo_url: Optional[str] = None
    short_description: Optional[str] = None
    
    # New fields
    enrollment: Optional[int] = None
    sat_score: Optional[int] = None
    act_score: Optional[int] = None
    graduation_rate: Optional[float] = None
    campus_setting: Optional[str] = None
    campus_images: Optional[str] = None # Will be stored as JSON string but we might want to parse it? Or keeps simple string for now.
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class College(CollegeBase):
    id: int
    degrees: List[Degree] = []

    
    class Config:
        from_attributes = True

class SalaryDataBase(BaseModel):
    median_salary_1yr: int
    median_salary_5yr: int

class SalaryData(SalaryDataBase):
    id: int
    college_id: int
    degree_id: int

    class Config:
        from_attributes = True
