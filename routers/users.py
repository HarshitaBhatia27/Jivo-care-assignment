from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

# all user related routes will be grouped under /users
router = APIRouter(prefix="/users", tags=["User Profile"])

# POST /users - create a new user profile
@router.post("/", response_model=schemas.UserProfileResponse)
def create_user(user: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    # checking if user with same name already exists
    existing = db.query(models.UserProfile).filter(models.UserProfile.name == user.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this name already exists")

    # creates new user object and save to database
    new_user = models.UserProfile(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# GET /users - get all users
@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.UserProfile).all()
    return users

# GET /users/{id} - get one user by id
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# DELETE /users/{id} - delete a user
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}