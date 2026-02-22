from fastapi import APIRouter
import json
import os

# meal routes for browsing the meal dataset
router = APIRouter(prefix="/meals", tags=["Meals"])

# helper to load meals from json file
def load_meals():
    file_path = os.path.join(os.path.dirname(__file__), "../data/meals.json")
    with open(file_path, "r") as f:
        return json.load(f)

# GET /meals - return all meals in the dataset
@router.get("/")
def get_all_meals():
    meals = load_meals()
    return {"total": len(meals), "meals": meals}

# GET /meals/filter?tag=veg - filter meals by dietary tag
@router.get("/filter")
def filter_meals_by_tag(tag: str):
    meals = load_meals()
    # return only meals that have the requested tag
    filtered = [m for m in meals if tag.lower() in m["tags"]]
    if not filtered:
        return {"message": f"No meals found for tag: {tag}", "meals": []}
    return {"total": len(filtered), "meals": filtered}