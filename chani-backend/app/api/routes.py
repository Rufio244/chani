from fastapi import APIRouter
from app.models.schemas import ChatRequest
from app.core.orchestrator import run_task

router = APIRouter()

@router.post("/chat")
async def chat(req: ChatRequest):
    result = await run_task(req.message)
    return {"result": result}
