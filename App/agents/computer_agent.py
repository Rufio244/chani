from app.services.openai_service import call_openai
from app.agents.computer_tools import *

async def run_computer_agent(goal: str):
    prompt = f"""
    คุณคือ AI ควบคุมคอม

    เป้าหมาย: {goal}

    ตอบเป็นคำสั่ง:
    ACTION:type:ข้อความ
    ACTION:open:web_url
    ACTION:key:enter
    ACTION:click:x,y
    ACTION:app:ชื่อโปรแกรม

    ทำทีละ step เดียว
    """

    action = await call_openai(prompt)

    if action.startswith("ACTION:type:"):
        return type_text(action.replace("ACTION:type:", ""))

    if action.startswith("ACTION:open:"):
        return open_website(action.replace("ACTION:open:", ""))

    if action.startswith("ACTION:key:"):
        return press_key(action.replace("ACTION:key:", ""))

    if action.startswith("ACTION:click:"):
        coords = action.replace("ACTION:click:", "")
        x, y = map(int, coords.split(","))
        return click(x, y)

    if action.startswith("ACTION:app:"):
        return open_app(action.replace("ACTION:app:", ""))

    return action
