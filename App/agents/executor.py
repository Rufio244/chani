from app.services.openai_service import call_openai
from app.agents.tools import web_search, save_file

async def execute_task(task: str):
    # ให้ AI เลือกว่าจะใช้ tool หรือคิดเอง
    prompt = f"""
    งาน: {task}

    ถ้าต้องใช้ tool ให้ตอบแบบ:
    TOOL:search:คำค้น
    หรือ
    TOOL:save:filename|content

    ถ้าไม่ใช้ tool ให้ตอบผลลัพธ์เลย
    """

    result = await call_openai(prompt)

    if result.startswith("TOOL:search:"):
        query = result.replace("TOOL:search:", "")
        return web_search(query)

    if result.startswith("TOOL:save:"):
        data = result.replace("TOOL:save:", "")
        filename, content = data.split("|")
        return save_file(filename, content)

    return result
