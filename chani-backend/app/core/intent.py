def analyze_intent(text: str):
    if "ค้นหา" in text or "search" in text:
        return {"type": "search"}
    if "ทำงาน" in text or "workflow" in text:
        return {"type": "automation"}
    return {"type": "generate"}
