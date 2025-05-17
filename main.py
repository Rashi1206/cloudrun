from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import uvicorn

app = FastAPI()

# Enable CORS to allow embedding on websites
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API setup
genai.configure(
    vertex_ai=True,
    project="mywebsitebot-dkju",
    location="us-central1",
)

@app.post("/generate")
async def generate_code(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt", "Write a Python algorithm for breast cancer detection")

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_prompt)]
        ),
    ]

    system_instruction = """You are an expert in coding algorithms, tutoring a college undergrad working on a group project in a programming class."""

    config = types.GenerateContentConfig(
        temperature=1,
        top_p=1,
        seed=0,
        max_output_tokens=2048,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        system_instruction=[types.Part.from_text(text=system_instruction)],
    )

    model = "gemini-2.5-pro-preview-05-06"

    # Stream output
    response = ""
    for chunk in genai.Client().models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        response += chunk.text

    return {"output": response}
