import json
import os

# load the meal data from our json file
def load_meals():
    file_path = os.path.join(os.path.dirname(__file__), "../data/meals.json")
    with open(file_path, "r") as f:
        return json.load(f)

# figure out how many calories the user needs per day by using a simple formula based on weight, height, age and activity level.
def calculate_daily_calories(weight, height, age, activity_level, goal):
    # basic BMR calculation 
    bmr = 10 * weight + 6.25 * height - 5 * age + 5

    # multiply by activity factor
    activity_factors = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725
    }
    factor = activity_factors.get(activity_level, 1.375)
    tdee = bmr * factor  # total daily energy expenditure

    # adjust based on goal
    if goal == "weight_loss":
        return tdee - 500  # eat 500 less to lose weight
    elif goal == "muscle_gain":
        return tdee + 300  # eat 300 more to build muscle
    else:
        return tdee  # maintenance, eat exactly what you burn

# filter meals that match the user's diet and goal
def filter_meals(meals, dietary_preference, health_goal, allergies):
    matched = []
    allergies_list = [a.strip().lower() for a in allergies.split(",")] if allergies else []

    for meal in meals:
        # skip if meal has allergen in name
        has_allergen = any(allergen in meal["name"].lower() for allergen in allergies_list)
        if has_allergen:
            continue

        # check if meal matches diet preference
        diet_match = dietary_preference in meal["tags"]

        # check if meal matches health goal
        goal_match = health_goal in meal["tags"]

        if diet_match or goal_match:
            matched.append(meal)

    return matched

# build a simple daily meal plan with breakfast lunch snack dinner
def build_daily_plan(filtered_meals, target_calories):
    breakfast = [m for m in filtered_meals if "breakfast" in m["tags"]]
    lunch = [m for m in filtered_meals if "lunch" in m["tags"]]
    snack = [m for m in filtered_meals if "snack" in m["tags"]]
    dinner = [m for m in filtered_meals if "dinner" in m["tags"]]

    # pick first available meal for each slot
    plan = {
        "breakfast": breakfast[0] if breakfast else None,
        "lunch": lunch[0] if lunch else None,
        "snack": snack[0] if snack else None,
        "dinner": dinner[0] if dinner else None
    }

    # calculate total calories in the plan
    total = sum(plan[slot]["calories"] for slot in plan if plan[slot])

    return {
        "target_calories": round(target_calories),
        "total_plan_calories": total,
        "meals": plan
    }

# main function that takes user profile and returns a meal plan
def get_recommendations(user):
    meals = load_meals()

    target_calories = calculate_daily_calories(
        user.weight_kg,
        user.height_cm,
        user.age,
        user.activity_level,
        user.health_goal
    )

    filtered = filter_meals(
        meals,
        user.dietary_preference,
        user.health_goal,
        user.allergies
    )

    daily_plan = build_daily_plan(filtered, target_calories)
    return daily_plan