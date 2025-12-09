from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import relationship
from .database import Base

# Many-to-Many association between College and Degree
college_degree_association = Table(
    "college_degree",
    Base.metadata,
    Column("college_id", Integer, ForeignKey("colleges.id")),
    Column("degree_id", Integer, ForeignKey("degrees.id")),
)

# Favorites Association
favorites = Table(
    "favorites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("college_id", Integer, ForeignKey("colleges.id"))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_premium = Column(Boolean, default=False)
    
    favorites = relationship("College", secondary=favorites)
    career_matches = relationship("CareerMatch", back_populates="user")

class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    admission_rate = Column(Float)  # stored as decimal 0.0-1.0
    avg_cost = Column(Integer)
    ranking = Column(Integer)
    website_url = Column(String)
    image_url = Column(String)
    logo_url = Column(String, nullable=True)  # College-specific logo
    short_description = Column(String, nullable=True) # Known For / Highlights
    
    # New fields
    enrollment = Column(Integer, nullable=True)
    sat_score = Column(Integer, nullable=True)
    act_score = Column(Integer, nullable=True)
    graduation_rate = Column(Float, nullable=True)
    campus_setting = Column(String, nullable=True)
    campus_images = Column(String, nullable=True) # JSON list of URLs
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    degrees = relationship("Degree", secondary=college_degree_association, back_populates="colleges")
    salary_data = relationship("SalaryData", back_populates="college")




class Degree(Base):
    __tablename__ = "degrees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String)  # e.g., "Bachelors", "Masters"

    colleges = relationship("College", secondary=college_degree_association, back_populates="degrees")

class SalaryData(Base):
    __tablename__ = "salary_data"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    degree_id = Column(Integer, ForeignKey("degrees.id"))
    median_salary_1yr = Column(Integer)
    median_salary_5yr = Column(Integer)

    college = relationship("College", back_populates="salary_data")
    degree = relationship("Degree")

class CareerMatch(Base):
    __tablename__ = "career_matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    career_title = Column(String)
    match_score = Column(Integer)
    created_at = Column(String)  # ISO timestamp
    
    user = relationship("User", back_populates="career_matches")
