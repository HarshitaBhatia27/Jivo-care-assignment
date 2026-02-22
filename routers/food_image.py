from fastapi import APIRouter, UploadFile, File
import base64
import httpx
import os

router = APIRouter(prefix="/food-analysis", tags=["Food Image Analysis"])

# using Clarifai's free food recognition model. It identifies food items from images and we map them to nutrition data
CLARIFAI_API_KEY = os.getenv("CLARIFAI_API_KEY", "")

# a simple nutrition lookup table for common indian foods
# in a production system this would come from a proper nutrition database
NUTRITION_MAP = {
    "rice": {"calories": 206, "protein": 4, "carbs": 45, "fat": 0.4},
    "bread": {"calories": 150, "protein": 5, "carbs": 28, "fat": 2},
    "chicken": {"calories": 239, "protein": 27, "carbs": 0, "fat": 14},
    "egg": {"calories": 155, "protein": 13, "carbs": 1, "fat": 11},
    "banana": {"calories": 89, "protein": 1, "carbs": 23, "fat": 0.3},
    "apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2},
    "dal": {"calories": 116, "protein": 9, "carbs": 20, "fat": 0.4},
    "paneer": {"calories": 265, "protein": 18, "carbs": 3, "fat": 20},
    "roti": {"calories": 120, "protein": 3, "carbs": 25, "fat": 1},
    "salad": {"calories": 50, "protein": 2, "carbs": 8, "fat": 0.5},
    "curry": {"calories": 180, "protein": 8, "carbs": 15, "fat": 9},
    "fish": {"calories": 208, "protein": 28, "carbs": 0, "fat": 10},
    "oats": {"calories": 158, "protein": 6, "carbs": 27, "fat": 3},
    "yogurt": {"calories": 100, "protein": 9, "carbs": 11, "fat": 2},
}

def get_nutrition(food_name: str):
    # try to match the detected food to our nutrition table
    food_lower = food_name.lower()
    for key in NUTRITION_MAP:
        if key in food_lower:
            return NUTRITION_MAP[key]
    # if no match found return a generic estimate
    return {"calories": 200, "protein": 5, "carbs": 30, "fat": 8}

# POST /food-analysis - upload a food image and get nutrition breakdown
@router.post("/")
async def analyze_food_image(file: UploadFile = File(...)):
    # read the uploaded image and convert to base64
    # clarifai API expects images in base64 format
    image_data = await file.read()
    encoded = base64.b64encode(image_data).decode("utf-8")

    if not CLARIFAI_API_KEY:
        # if no API key is set, return a mock response for testing
        return {
            "note": "Clarifai API key not set. Returning mock response.",
            "food_detected": "Dal Rice",
            "nutrition_per_serving": {
                "calories": 420,
                "protein": 17,
                "carbs": 68,
                "fat": 6
            }
        }

    # call clarifai food recognition API
    headers = {
        "Authorization": f"Key {CLARIFAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": [{
            "data": {
                "image": {"base64": encoded}
            }
        }]
    }

    # using clarifai's food model
    url = "https://api.clarifai.com/v2/models/food-item-recognition/outputs"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        return {"error": "Could not analyze image", "detail": response.text}

    # parse the top detected food from response
    result = response.json()
    concepts = result["outputs"][0]["data"]["concepts"]
    top_food = concepts[0]["name"] if concepts else "unknown"

    # get nutrition info for detected food
    nutrition = get_nutrition(top_food)

    return {
        "food_detected": top_food,
        "confidence": round(concepts[0]["value"] * 100, 2),
        "nutrition_per_serving": nutrition
    }