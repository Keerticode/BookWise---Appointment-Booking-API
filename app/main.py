from fastapi import FastAPI

from app.routers import users, services, appointments, availability

app = FastAPI()


app.include_router(users.router)
app.include_router(services.router)
app.include_router(appointments.router)
app.include_router(availability.router)

@app.get("/")
def root() :
    return {"message" : "Welcome to BookWise API"}