from sqlalchemy import Column, Integer, String
from database import Base


class Interview(Base):

    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    role = Column(String)

    skills = Column(String)

    questions = Column(String)