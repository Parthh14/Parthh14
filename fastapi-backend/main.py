from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS Middleware to allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Replace "*" with the frontend URL in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# In-memory database to store users
users_db = []

# Pydantic models
class User(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# Root route
@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI backend!"}

# Sign-Up API
@app.post("/signup")
def sign_up(user: User):
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    users_db.append(user.dict())
    return {"message": "User registered successfully"}

# Sign-In API
@app.post("/signin")
def sign_in(request: LoginRequest):
    for user in users_db:
        if user["email"] == request.email and user["password"] == request.password:
            return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid email or password")

# List Users API
@app.get("/users", response_model=List[User])
def list_users():
    return users_db
