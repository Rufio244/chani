#!/bin/bash

# CHANI AUTO DEPLOY SYSTEM
# GitHub + Server Bootstrap

set -e

REPO=$1
TOKEN=$2

echo "🧠 Starting Chani Deployment..."

# install tools
sudo apt update
sudo apt install -y git python3 python3-pip

# create project
mkdir -p chani && cd chani

cat > chani_core.py <<'PY'
from fastapi import FastAPI
import uvicorn

app = FastAPI()

memory = []

@app.get("/")
def home():
    return {
        "system":"CHANI",
        "status":"online"
    }

@app.post("/learn")
def learn(data:dict):
    memory.append(data)
    return {
        "saved":True,
        "memory_size":len(memory)
    }

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=7777)
PY


cat > requirements.txt <<EOF
fastapi
uvicorn
EOF

pip3 install -r requirements.txt


# github connect

git init

git config --global user.name "Chani-AI"
git config --global user.email "chani@system.ai"

git add .
git commit -m "Initialize Chani Core"


REMOTE=https://${TOKEN}@github.com/${REPO}.git

git branch -M main
git remote add origin $REMOTE
git push -u origin main


# auto updater

cat > update.sh <<'EOF'
#!/bin/bash
git pull
pip3 install -r requirements.txt
systemctl restart chani
EOF

chmod +x update.sh


# service

sudo tee /etc/systemd/system/chani.service <<EOF
[Unit]
Description=Chani AI Core

[Service]
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/chani_core.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF


sudo systemctl daemon-reload
sudo systemctl enable chani
sudo systemctl start chani


echo "✅ CHANI ONLINE"
echo "API: http://SERVER_IP:7777"
