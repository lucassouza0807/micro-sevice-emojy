from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.services.OpenIAservice import emojifyPhrase
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/ping")
async def ping(request: Request):
    response = {
        "message": "Ok"
    }
    
    return JSONResponse(content=response)

@app.post("/api/emojify")
async def emojify(request: Request):
    try:
        body = await request.json()
        
        if 'phrase' not in body:
            raise HTTPException(status_code=400, detail="O campo 'phrase' não foi encontrado no corpo da requisição.")
        
        emojified_phrase = await emojifyPhrase(body['phrase'])
        
        response = {
            "original_phrase": body["phrase"],
            "emojified_phrase": emojified_phrase
        }
        
        return JSONResponse(content=response) 
        
    except Exception as e:
         return JSONResponse(
            status_code=500,
            content={"error": f"An unexpected error occurred: {str(e)}"}
        )
