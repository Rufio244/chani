from app.core.intent import analyze_intent
from app.services.openai_service import call_openai
from app.services.workflow_service import run_workflow

async def run_task(message: str):
    intent = analyze_intent(message)

    if intent["type"] == "generate":
        return await call_openai(message)

    if intent["type"] == "automation":
        return await run_workflow(message)

    if intent["type"] == "search":
        return f"Search result for: {message}"

    return "Unknown task"
