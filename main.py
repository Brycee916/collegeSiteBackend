from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, auth, colleges, careers, career_matches

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="College Finder API", description="API for searching and ranking colleges", version="1.0.0")

# CORS middleware to allow requests from the React frontend
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5199",
    "http://localhost:5200",
    "http://localhost:5205",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(colleges.router, tags=["Colleges"])
app.include_router(careers.router, tags=["Careers"])
app.include_router(career_matches.router, tags=["Career Matches"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the College Finder API"}
