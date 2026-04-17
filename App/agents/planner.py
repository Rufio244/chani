from app.services.openai_service import call_openai
import json

async def create_plan(goal: str):
    prompt = f"""
    แปลงเป้าหมายนี้เป็นขั้นตอน:
    "{goal}"

    ตอบเป็น JSON array:
    ["task1", "task2", "task3"]
    """

    result = await call_openai(prompt)

    try:
        return json.loads(result)
    except:
        return [goal]
