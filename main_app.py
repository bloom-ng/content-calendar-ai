from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
from typing import List
from predict_function import predict  # Change this line to import 'predict'
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()  # Add this line to create the FastAPI instance

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str

class PredictRequest(BaseModel):
    message: str

class PredictResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-groq-70b-8192-tool-use-preview",
        "messages": request.messages,
        "temperature": 1.25,
        "max_tokens": 8192,
        "top_p": 0.5,
        "stop": None
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(GROQ_API_URL, json=payload, headers=headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from Groq API: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with Groq API: {str(e)}")
    
    response_data = response.json()
    chatbot_response = response_data['choices'][0]['message']['content']
    
    return ChatResponse(response=chatbot_response)

@app.post("/predict", response_model=PredictResponse)
async def predict_endpoint(request: PredictRequest):
    try:
        # You might need to adjust this call depending on how you want to handle the 'history' parameter
        response = predict(request.message, history=[])
        return PredictResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in prediction: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)