from database import SessionLocal, engine
from crud import create_interview
from models import Base

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import tempfile
import os

app = FastAPI()

# ---------------------------------
# CORS (Frontend connection)
# ---------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------
# Create database tables
# ---------------------------------
Base.metadata.create_all(bind=engine)


# ---------------------------------
# Home route
# ---------------------------------
@app.get("/")
def home():
    return {"message": "Backend Working"}


# ---------------------------------
# Skill extraction
# ---------------------------------
def extract_skills(text):

    skills = []

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

    for skill in skill_keywords:

        if skill.lower() in text.lower():
            skills.append(skill)

    return skills


# ---------------------------------
# Question generation
# ---------------------------------
def generate_questions(role):

    questions = []

    try:

        with open(
            "knowledge_base/aiml_notes.txt",
            "r",
            encoding="utf-8"
        ) as file:

            knowledge = file.read()

    except:

        knowledge = ""


    if role == "AI/ML Engineer":

        if "Overfitting" in knowledge:
            questions.append(
                "What is overfitting and why does it happen?"
            )

        if "Train-test split" in knowledge:
            questions.append(
                "Why do we use train-test split?"
            )

        if "EDA" in knowledge:
            questions.append(
                "Why is EDA important?"
            )

        if len(questions) == 0:

            questions = [
                "Explain overfitting in machine learning.",
                "What is train_test_split used for?",
                "Why is EDA important?"
            ]

    elif role == "Backend Engineer":

        questions = [
            "What is FastAPI?",
            "Difference between GET and POST?"
        ]

    return questions


# ---------------------------------
# Upload Resume Route
# ---------------------------------
@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    role: str = Form(...)
):

    temp_path = None

    try:

        # Save temporary PDF
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp:

            temp.write(
                await file.read()
            )

            temp_path = temp.name


        # Read PDF
        reader = PdfReader(temp_path)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted


        # Extract skills
        skills = extract_skills(text)

        # Generate questions
        questions = generate_questions(role)


        # Save database
        db = SessionLocal()

        try:

            create_interview(
                db=db,
                filename=file.filename,
                role=role,
                skills=", ".join(skills),
                questions=", ".join(questions)
            )

        finally:
            db.close()


        return {

            "filename": file.filename,
            "role": role,
            "skills": skills,
            "interview_questions": questions

        }

    except Exception as e:

        return {
            "error": str(e)
        }

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)