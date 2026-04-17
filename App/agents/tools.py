import requests

def web_search(query: str):
    return f"ผลการค้นหา: {query}"

def save_file(filename: str, content: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"saved {filename}"
