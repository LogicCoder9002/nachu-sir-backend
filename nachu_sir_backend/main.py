from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from fastapi.middleware.cors import CORSMiddleware

# Load the Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("AIzaSyAlduAXniEIx7ugU8lBYDE8kIP231Pka7s")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please add it as an environment variable.")

genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GrammarQuery(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: GrammarQuery):
    """Handles grammar-related questions using Gemini AI."""
    try:
        response = genai.generate_text(query.question)
        return {"answer": response["candidates"][0]["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Nachu Sir Backend is Running!"}
