from database import SessionLocal, engine
from crud import create_interview
from models import Base

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader

import tempfile
import os

app = FastAPI()

# -------------------------------
# CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Create DB Tables
# -------------------------------
Base.metadata.create_all(bind=engine)

# -------------------------------
# Home Route
# -------------------------------
@app.get("/")
def home():
    return {"message": "Backend Working"}

# -------------------------------
# Skills Extraction
# -------------------------------
def extract_skills(text):

    skill_keywords = [
        "Python",
        "SQL",
        "Machine Learning",
        "NumPy",
        "Pandas",
        "Scikit-learn",
        "FastAPI",
        "Git",
        "EDA"
    ]

    found_skills = []

    for skill in skill_keywords:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills

# -------------------------------
# Question Generator
# -------------------------------
def generate_questions(role):

    if role == "Backend Engineer":
        return [
            "What is FastAPI?",
            "Difference between GET and POST?",
            "What is REST API?",
            "Explain dependency injection."
        ]

    return [
        "Explain overfitting in machine learning.",
        "What is train_test_split used for?",
        "Why is EDA important?",
        "Difference between supervised and unsupervised learning?"
    ]

# -------------------------------
# Upload Resume
# -------------------------------
@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    role: str = Form(...)
):

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp:

            temp.write(await file.read())
            temp_path = temp.name

        reader = PdfReader(temp_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

        skills = extract_skills(text)

        questions = generate_questions(role)

        db = SessionLocal()

        try:
            create_interview(
                db=db,
                filename=file.filename,
                role=role,
                skills=", ".join(skills),
                questions=", ".join(questions)
            )

        except Exception as db_error:
            print("Database Error:", db_error)

        finally:
            db.close()

        return {
            "filename": file.filename,
            "role": role,
            "skills": skills,
            "interview_questions": questions
        }

    except Exception as e:

        print("UPLOAD ERROR:", str(e))

        return {
            "error": str(e)
        }

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)