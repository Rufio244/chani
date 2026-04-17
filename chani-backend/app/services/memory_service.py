memory_store = []

def save_memory(text: str):
    memory_store.append(text)

def get_memory():
    return memory_store[-5:]
