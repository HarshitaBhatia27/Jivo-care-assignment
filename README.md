# JivoCare Diet Recommendation API

A backend service that generates personalized daily meal plans based on user health profiles. Built with FastAPI and MySQL.

## What This Does

- User creates a profile with age, weight, height, activity level, diet preference and health goal
- System calculates daily calorie target using Mifflin-St Jeor formula
- Returns a personalized meal plan with breakfast, lunch, snack and dinner
- Supports food image upload to get estimated nutritional breakdown

## Project Structure
```

jivo-care-assignment/
├── main.py               # app entry point, registers all routes
├── database.py           # mysql connection setup
├── models.py             # database table definitions
├── schemas.py            # request and response validation
├── routers/
│   ├── users.py          # user profile APIs
│   ├── meals.py          # meal browsing APIs
│   ├── recommendations.py # meal plan generation
│   └── food_image.py     # food image analysis
├── ml/
│   └── recommender.py    # calorie calculation + meal matching logic
├── data/
│   └── meals.json        # indian meal dataset with nutrition info
└── requirements.txt
```


## Tech Stack

- Python 3.10
- FastAPI — API framework
- Uvicorn — ASGI server to run FastAPI
- SQLAlchemy — ORM for database operations
- MySQL — stores user profiles
- Mifflin-St Jeor formula — calorie target calculation

## Setup Steps

**1. Clone the repo**
```bash
git clone <your-repo-link>
cd jivo-care-assignment
```

**2. Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create MySQL database**
```bash
mysql -u root -p
CREATE DATABASE jivocare;
EXIT;
```

**5. Create .env file in root folder**
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=jivocare
```

**6. Run the server**
```bash
uvicorn main:app --reload
```

**7. Open API docs**
```
http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /users/ | Create user profile |
| GET | /users/ | Get all users |
| GET | /users/{id} | Get user by ID |
| DELETE | /users/{id} | Delete user |
| GET | /meals/ | Get all meals |
| GET | /meals/filter?tag=veg | Filter meals by tag |
| GET | /recommendations/{user_id} | Get daily meal plan |
| POST | /food-analysis/ | Upload food image for nutrition info |

## Sample Request — Create User
```json
POST /users/
{
  "name": "Dev",
  "age": 28,
  "height_cm": 175,
  "weight_kg": 75,
  "activity_level": "active",
  "dietary_preference": "non-veg",
  "health_goal": "muscle_gain",
  "allergies": null,
  "health_conditions": null
}
```

## Sample Response — Get Recommendation
```json
GET /recommendations/1
{
  "user": "Dev",
  "goal": "muscle_gain",
  "diet": "non-veg",
  "daily_plan": {
    "target_calories": 2800,
    "plan_calories": 1280,
    "note": "Calorie target is approximate. Consult a nutritionist for medical advice.",
    "meals": {
      "breakfast": {
        "name": "Chicken Egg White Omelette",
        "calories": 260,
        "protein": 32,
        "carbs": 4,
        "fat": 10
      },
      "lunch": {
        "name": "Chicken Curry with Roti",
        "calories": 480,
        "protein": 38,
        "carbs": 42,
        "fat": 14
      },
      "snack": {
        "name": "Whey Protein with Milk",
        "calories": 220,
        "protein": 30,
        "carbs": 12,
        "fat": 4
      },
      "dinner": {
        "name": "Grilled Tandoori Chicken",
        "calories": 320,
        "protein": 42,
        "carbs": 8,
        "fat": 10
      }
    }
  }
}
```

## Recommendation Logic

1. Calculate BMR using Mifflin-St Jeor formula
2. Multiply by activity factor to get TDEE (total daily energy expenditure)
3. Adjust for goal — subtract 500 calories for weight loss, add 300 for muscle gain
4. Filter meals that match dietary preference and health goal tags
5. Pick one meal per time slot — breakfast, lunch, snack, dinner

## Food Image Analysis

Upload any food image to `/food-analysis/` endpoint.
Returns estimated food name, calories, protein, carbs and fat.
Uses Clarifai food recognition API when API key is set.
Returns a mock response for testing without an API key.

## Activity Levels

| Level | Description |
|-------|-------------|
| sedentary | desk job, little or no exercise |
| light | light exercise 1-3 days a week |
| moderate | moderate exercise 3-5 days a week |
| active | hard exercise 6-7 days a week |

## Health Goals

| Goal | Calorie Adjustment |
|------|--------------------|
| weight_loss | TDEE - 500 calories |
| muscle_gain | TDEE + 300 calories |
| maintenance | TDEE (no change) |