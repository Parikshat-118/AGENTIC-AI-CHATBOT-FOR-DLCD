from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import rag
from .routers import pdfs
from .routers import quizzes   

app = FastAPI(
    title="Electronics Learning AI Backend",
    version="1.1.0",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.8:3000",
    "http://192.168.1.4:3000",
    "http://10.25.43.144:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

# Routers
app.include_router(rag.router, prefix="/rag", tags=["rag"])
app.include_router(pdfs.router, tags=["pdfs"])
app.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])  
