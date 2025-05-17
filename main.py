from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow CORS (for embedding in GoDaddy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/execute")
async def execute(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    
    # --- Your model logic goes here ---
    result = f"Processed: {prompt}"  # Replace with your real logic
    return {"output": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
