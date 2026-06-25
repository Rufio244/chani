from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import sqlite3
import datetime


app = FastAPI(
    title="Chani AGI Gateway"
)


SECRET_KEY = "CHANI_KEY_001"


db = sqlite3.connect(
    "chani_memory.db",
    check_same_thread=False
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory(
id TEXT,
data TEXT,
source TEXT,
time TEXT
)
""")

db.commit()



class AGIRequest(BaseModel):
    command:str
    data:str=None
    code:str=None



def check_key(key):

    if key != SECRET_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid AGI Key"
        )



@app.post("/agi")
def agi_command(
    req:AGIRequest,
    x_agi_key:str=Header(None)
):

    check_key(x_agi_key)


    command=req.command


    # บันทึกข้อมูลเข้า Chani

    if "บันทึก" in command:

        cursor.execute(
        """
        INSERT INTO memory
        VALUES(?,?,?,?)
        """,
        (
        req.code,
        req.data,
        "external",
        str(datetime.datetime.now())
        ))

        db.commit()


        return {
        "status":"saved",
        "code":req.code
        }



    # ดึงข้อมูลจาก Chani

    if "ดึงข้อมูล" in command:

        cursor.execute(
        """
        SELECT * FROM memory
        WHERE id=?
        """,
        (req.code,)
        )

        result=cursor.fetchall()


        return {
        "memory":result
        }



    # คำสั่งวิเคราะห์

    if "วิเคราะห์" in command:

        return {

        "task":
        "ส่งข้อมูลไป AI Engine",

        "input":
        req.data,

        "code":
        req.code

        }



    return {

    "status":"unknown command"

    }
