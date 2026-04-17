from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Chani AI")

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"status": "Chani running"}
