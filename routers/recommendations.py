from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from ml.recommender import get_recommendations
import models

# recommendation routes is the core feature of the service
router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

# GET /recommendations/{user_id} get meal plan for a specific user
@router.get("/{user_id}")
def recommend_meals(user_id: int, db: Session = Depends(get_db)):
    # first fetch the user profile from database
    user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # pass user profile to recommendation engine
    plan = get_recommendations(user)

    return {
        "user": user.name,
        "goal": user.health_goal,
        "diet": user.dietary_preference,
        "daily_plan": plan
    }