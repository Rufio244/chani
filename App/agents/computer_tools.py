import pyautogui
import webbrowser
import time
import os

pyautogui.FAILSAFE = True

def open_app(app_name: str):
    os.system(f"start {app_name}")
    return f"เปิด {app_name}"

def type_text(text: str):
    pyautogui.write(text, interval=0.05)
    return f"พิมพ์: {text}"

def press_key(key: str):
    pyautogui.press(key)
    return f"กดปุ่ม {key}"

def open_website(url: str):
    webbrowser.open(url)
    return f"เปิดเว็บ {url}"

def click(x: int, y: int):
    pyautogui.click(x, y)
    return f"คลิกที่ {x},{y}"

def screenshot(filename="screen.png"):
    img = pyautogui.screenshot()
    img.save(filename)
    return f"saved {filename}"
