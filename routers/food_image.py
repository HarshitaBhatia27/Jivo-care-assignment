from fastapi import APIRouter, UploadFile, File
from PIL import Image
import numpy as np
import io

router = APIRouter(prefix="/food-analysis", tags=["Food Image Analysis"])

# nutrition lookup for common foods
NUTRITION_MAP = {
    "pizza": {"calories": 285, "protein": 12, "carbs": 36, "fat": 10},
    "hamburger": {"calories": 354, "protein": 20, "carbs": 29, "fat": 17},
    "hotdog": {"calories": 290, "protein": 10, "carbs": 24, "fat": 18},
    "french fries": {"calories": 312, "protein": 3, "carbs": 41, "fat": 15},
    "ice cream": {"calories": 207, "protein": 4, "carbs": 24, "fat": 11},
    "cake": {"calories": 350, "protein": 4, "carbs": 55, "fat": 14},
    "donut": {"calories": 452, "protein": 5, "carbs": 51, "fat": 25},
    "sandwich": {"calories": 300, "protein": 15, "carbs": 35, "fat": 10},
    "rice": {"calories": 206, "protein": 4, "carbs": 45, "fat": 0.4},
    "chicken": {"calories": 239, "protein": 27, "carbs": 0, "fat": 14},
    "egg": {"calories": 155, "protein": 13, "carbs": 1, "fat": 11},
    "banana": {"calories": 89, "protein": 1, "carbs": 23, "fat": 0.3},
    "apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2},
    "broccoli": {"calories": 55, "protein": 4, "carbs": 11, "fat": 0.6},
    "carrot": {"calories": 41, "protein": 1, "carbs": 10, "fat": 0.2},
    "corn": {"calories": 86, "protein": 3, "carbs": 19, "fat": 1.4},
    "spaghetti": {"calories": 220, "protein": 8, "carbs": 43, "fat": 1.3},
    "soup": {"calories": 150, "protein": 6, "carbs": 18, "fat": 5},
    "salad": {"calories": 50, "protein": 2, "carbs": 8, "fat": 0.5},
    "bread": {"calories": 150, "protein": 5, "carbs": 28, "fat": 2},
    "dal": {"calories": 116, "protein": 9, "carbs": 20, "fat": 0.4},
    "paneer": {"calories": 265, "protein": 18, "carbs": 3, "fat": 20},
    "roti": {"calories": 120, "protein": 3, "carbs": 25, "fat": 1},
    "curry": {"calories": 180, "protein": 8, "carbs": 15, "fat": 9},
    "biryani": {"calories": 290, "protein": 10, "carbs": 45, "fat": 8},
    "samosa": {"calories": 262, "protein": 5, "carbs": 32, "fat": 13},
    "idli": {"calories": 58, "protein": 2, "carbs": 12, "fat": 0.4},
    "dosa": {"calories": 168, "protein": 4, "carbs": 30, "fat": 4},
    "naan": {"calories": 317, "protein": 9, "carbs": 55, "fat": 7},
    "khichdi": {"calories": 360, "protein": 12, "carbs": 62, "fat": 8},
}

def get_nutrition(food_name: str):
    # check if detected food matches anything in our map
    food_lower = food_name.lower()
    for key in NUTRITION_MAP:
        if key in food_lower:
            return NUTRITION_MAP[key]
    # generic estimate if food not in our database
    return {"calories": 200, "protein": 5, "carbs": 30, "fat": 8}

def load_model():
    # using MobileNetV2 pretrained on ImageNet
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
    model = MobileNetV2(weights="imagenet")
    return model, preprocess_input, decode_predictions

# load model once when server starts
print("Loading MobileNetV2 model...")
model, preprocess_input, decode_predictions = load_model()
print("Model loaded!")

@router.post("/")
async def analyze_food_image(file: UploadFile = File(...)):
    # read uploaded image
    image_data = await file.read()

    # open and preprocess the image for MobileNetV2
    img = Image.open(io.BytesIO(image_data)).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # run prediction
    predictions = model.predict(img_array)

    # decode top 3 predictions from ImageNet classes
    top_preds = decode_predictions(predictions, top=3)[0]

    # top prediction
    top_food = top_preds[0][1].replace("_", " ")
    confidence = round(float(top_preds[0][2]) * 100, 2)

    # all top 3 for context
    top_3 = [
        {"food": p[1].replace("_", " "), "confidence": round(float(p[2]) * 100, 2)}
        for p in top_preds
    ]

    # get nutrition info
    nutrition = get_nutrition(top_food)

    return {
        "food_detected": top_food,
        "confidence_percent": confidence,
        "other_possibilities": top_3,
        "nutrition_per_serving": nutrition,
        "note": "Nutrition values are estimates per standard serving size"
    }