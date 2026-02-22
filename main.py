from fastapi import FastAPI
from database import engine, Base
from routers import users, meals, recommendations, food_image

# create all database tables on startup
# SQLAlchemy reads our models and creates the tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JivoCare Diet Recommendation API",
    description="A backend service that generates personalized meal plans based on user health profiles",
    version="1.0.0"
)

# register all route modules
app.include_router(users.router)
app.include_router(meals.router)
app.include_router(recommendations.router)
app.include_router(food_image.router)

# health check endpoint
@app.get("/")
def root():
    return {
        "service": "JivoCare Diet Recommendation API",
        "status": "running",
        "docs": "/docs"
    }