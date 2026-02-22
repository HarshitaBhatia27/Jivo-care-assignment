from sqlalchemy import Column, Integer, String, Float, Text
from database import Base


# this class represents the user_profiles table in MySQL, each variable here becomes a column in the table
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    age = Column(Integer)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    activity_level = Column(String(50))  # sedentary, light, moderate, active
    dietary_preference = Column(String(50))  # veg, vegan, keto, non-veg
    health_goal = Column(String(50))  # weight_loss, muscle_gain, maintenance
    allergies = Column(Text, nullable=True)
    health_conditions = Column(Text, nullable=True)