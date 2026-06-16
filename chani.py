import os
import secrets
import datetime

from fastapi import FastAPI, Header, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

openai.api_key=OPENAI_API_KEY

app=FastAPI(title="ChaNi AI")

# memory database
users={}
api_keys={}
usage_logs=[]

# -------- USER SYSTEM ----------

def create_user(email,password):

    users[email]={
        "password":password,
        "keys":[]
    }

# -------- API KEY SYSTEM -------

def generate_key(email):

    key="chani_sk_"+secrets.token_hex(16)

    api_keys[key]=email

    users[email]["keys"].append(key)

    return key

# -------- AI CHAT --------------

def ai_chat(message):

    res=openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":message}]
    )

    reply=res["choices"][0]["message"]["content"]
    tokens=res["usage"]["total_tokens"]

    return reply,tokens

# --------- MODELS -------------

class ChatRequest(BaseModel):
    message:str

# --------- API ----------------

@app.post("/v1/chat")
def chat(req:ChatRequest,authorization:str=Header(None)):

    if not authorization:
        return {"error":"missing key"}

    key=authorization.replace("Bearer ","")

    if key not in api_keys:
        return {"error":"invalid key"}

    reply,tokens=ai_chat(req.message)

    usage_logs.append({
        "key":key,
        "tokens":tokens,
        "time":str(datetime.datetime.utcnow())
    })

    return {"reply":reply}

# --------- WEBSITE ------------

@app.get("/",response_class=HTMLResponse)
def home():

    return """

<html>

<head>

<title>ChaNi AI</title>

<style>

body{
background:#0f172a;
color:white;
font-family:Arial;
text-align:center;
}

input,textarea{
width:300px;
padding:10px;
margin:5px;
}

button{
padding:10px 20px;
background:#22c55e;
border:none;
color:white;
}

</style>

</head>

<body>

<h1>🚀 ChaNi AI Platform</h1>

<h2>Create User</h2>

<input id="email" placeholder="email"><br>
<input id="pass" placeholder="password"><br>

<button onclick="signup()">Signup</button>

<h2>Create API Key</h2>

<button onclick="createKey()">Create Key</button>

<p id="key"></p>

<h2>AI Chat</h2>

<textarea id="msg"></textarea><br>

<button onclick="chat()">Send</button>

<p id="reply"></p>

<script>

let apiKey=""

function signup(){

fetch("/signup",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
email:document.getElementById("email").value,
password:document.getElementById("pass").value
})
})

}

function createKey(){

fetch("/create-key",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
email:document.getElementById("email").value
})
})
.then(r=>r.json())
.then(d=>{

apiKey=d.key

document.getElementById("key").innerText=d.key

})

}

function chat(){

fetch("/v1/chat",{

method:"POST",

headers:{
"Content-Type":"application/json",
"Authorization":"Bearer "+apiKey
},

body:JSON.stringify({
message:document.getElementById("msg").value
})

})

.then(r=>r.json())
.then(d=>{

document.getElementById("reply").innerText=d.reply

})

}

</script>

</body>

</html>

"""

# ---------- SIGNUP ------------

@app.post("/signup")
async def signup(data:dict):

    create_user(data["email"],data["password"])

    return {"status":"user created"}

# ---------- CREATE KEY --------

@app.post("/create-key")
async def create_key(data:dict):

    key=generate_key(data["email"])

    return {"key":key}

# ---------- DASHBOARD ---------

@app.get("/dashboard")
def dashboard():

    return {
        "users":users,
        "keys":api_keys,
        "usage":usage_logs
    }
chani.py

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CHANI Semantic Core")

SEMANTIC = {
"ฉัน": {"id": "SEM-000001", "concept": "SELF"},
"ผม": {"id": "SEM-000001", "concept": "SELF"},
"I": {"id": "SEM-000001", "concept": "SELF"},

"ดื่ม": {"id": "ACT-000001", "concept": "DRINK"},
"drink": {"id": "ACT-000001", "concept": "DRINK"},

"น้ำ": {"id": "OBJ-000001", "concept": "WATER"},
"water": {"id": "OBJ-000001", "concept": "WATER"},

"เรียน": {"id": "ACT-000002", "concept": "LEARN"},
"learn": {"id": "ACT-000002", "concept": "LEARN"},

"สร้าง": {"id": "ACT-000003", "concept": "CREATE"},
"create": {"id": "ACT-000003", "concept": "CREATE"}

}

class TextInput(BaseModel):
text: str

@app.get("/")
def root():
return {
"name": "CHANI",
"status": "online",
"version": "1.0"
}

@app.get("/health")
def health():
return {
"status": "online",
"semantic_core": True
}

@app.post("/semantic/parse")
def semantic_parse(data: TextInput):

words = data.text.split()

concepts = []

for word in words:
    if word in SEMANTIC:
        concepts.append(SEMANTIC[word])

return {
    "input": data.text,
    "semantic": concepts
}

@app.post("/agi")
def agi(data: TextInput):

cmd = data.text.replace("#AGI", "").strip()

return {
    "gateway": "CHANI",
    "command": cmd,
    "status": "accepted"
    }
