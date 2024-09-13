# FastAPI Chat and Prediction API

This FastAPI application provides two main endpoints: one for chat completions using the Groq API, and another for custom predictions.

## Setup

1. Clone the repository and navigate to the project directory.

2. Install the required dependencies:
   ````
   pip install fastapi uvicorn httpx pydantic python-dotenv
   ```

3. Create a `.env` file in the project root and add your Groq API key:
   ````
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Ensure you have the `predict_function.py` file in the same directory as `main_app.py`.

## Running the API

To start the API server, run:

```
python main_app.py
```

The server will start on `http://0.0.0.0:8000`.

## API Endpoints

### 1. Chat Completion

**Endpoint:** `/chat`
**Method:** POST

**Request Body:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello, how are you?"
    }
  ]
}
```

**Response:**
```json
{
  "response": "AI-generated response here"
}
```

### 2. Custom Prediction

**Endpoint:** `/predict`
**Method:** POST

**Request Body:**
```json
{
  "message": "Your input message here"
}
```

**Response:**
```json
{
  "response": "Prediction result here"
}
```

## Error Handling

The API will return appropriate HTTP status codes and error messages for various scenarios, such as invalid input or API communication errors.

## Note

Make sure to keep your Groq API key confidential and not expose it in public repositories or client-side code.