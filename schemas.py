from pydantic import BaseModel #data validation library that works well with FastAPI to define the structure of our data and automatically validate it
from typing import Optional

# this is what the user sends when creating a profile and pydantic automatically validates the data types for us
class UserProfileCreate(BaseModel):
    name: str
    age: int
    height_cm: float
    weight_kg: float
    activity_level: str
    dietary_preference: str
    health_goal: str
    allergies: Optional[str] = None
    health_conditions: Optional[str] = None

class UserProfileResponse(UserProfileCreate):
    id: int
    class Config: 
        from_attributes = True # this allows SQLAlchemy model to be converted to pydantic response
