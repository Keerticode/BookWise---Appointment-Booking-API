from fastapi import FastAPI

from app.routers import users
from app.routers import services
from app.routers import appointments

app = FastAPI()


app.include_router(users.router)
app.include_router(services.router)
app.include_router(appointments.router)

@app.get("/")
def root() :
    return {"message" : "Welcome to BookWise API"}