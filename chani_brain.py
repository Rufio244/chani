#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧠 Chani Universal Brain Gateway v1
SINGLE FILE DEPLOYMENT

ความสามารถ:
- API Gateway
- Knowledge Memory
- External API Connector
- Learning Storage
- System Status
"""

from fastapi import FastAPI, Header
import requests
import time
import json
import hashlib
import uvicorn


# ==========================
# CONFIG
# ==========================

SYSTEM_NAME = "Chani Universal Brain Gateway"

API_KEY = "CHANI_SECURE_244"

MEMORY_FILE = "chani_memory.json"


# ==========================
# MEMORY ENGINE
# ==========================

class Memory:

    def __init__(self):

        try:
            with open(
                MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as f:
                self.data=json.load(f)

        except:

            self.data=[]


    def save(self,item):

        self.data.append(item)

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.data,
                f,
                ensure_ascii=False,
                indent=2
            )


    def all(self):

        return self.data



memory = Memory()



# ==========================
# BRAIN ENGINE
# ==========================

class ChaniBrain:


    def learn(self,data):

        knowledge={

            "id":
            hashlib.sha256(
                str(data).encode()
            ).hexdigest(),

            "content":
            data,

            "time":
            time.time(),

            "status":
            "stored"

        }


        memory.save(knowledge)

        return knowledge



brain = ChaniBrain()



# ==========================
# API SERVER
# ==========================

app = FastAPI(
    title=SYSTEM_NAME,
    version="1.0"
)



def security(key):

    return key == API_KEY



@app.get("/")
def home():

    return {

        "system":SYSTEM_NAME,

        "status":
        "ONLINE",

        "memory":
        len(memory.all())

    }



@app.post("/learn")
def learn(
    data:dict,
    x_api_key:str=Header(None)
):

    if not security(x_api_key):

        return {
            "error":
            "ACCESS_DENIED"
        }


    return brain.learn(data)



@app.get("/memory")
def get_memory(
    x_api_key:str=Header(None)
):

    if not security(x_api_key):

        return {
            "error":
            "ACCESS_DENIED"
        }


    return memory.all()



# ==========================
# EXTERNAL API CONNECTOR
# ==========================

@app.post("/connect")
def connect_api(
    url:str,
    x_api_key:str=Header(None)
):

    if not security(x_api_key):

        return {
            "error":
            "ACCESS_DENIED"
        }


    result=requests.get(url)


    return {

        "source":url,

        "data":
        result.json()

    }



# ==========================
# START
# ==========================

if __name__=="__main__":

    print(
        "🧠 Chani Brain Running..."
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
