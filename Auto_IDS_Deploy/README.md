# Automated Intrusion Detection System (IDS)
##  Real-Time AI-Based Threat Detection & Monitoring

This project implements an **AI-powered Intrusion Detection System (IDS)** with automated deployment using **GitHub Actions**, running on a **self-hosted Ubuntu VM (192.168.0.119)**. 

### �� Features
✔ **Live traffic simulation** with **Tcpreplay**  
✔ **AI-powered intrusion detection** using a trained **Neural Network Model**  
✔ **Real-time classification updates** displayed on a **Dash dashboard**  
✔ **Historical storage of traffic logs** using **MongoDB**  
✔ **Automated alerting mechanism** for detected threats  
✔ **Continuous Integration & Deployment (CI/CD) with GitHub Actions**  

---

## Project Folder Structure
```
cicids-automation/
│── .github/                
│   ├── workflows/                
│   │   ├── deploy-ids.yml    # GitHub Actions workflow
│── scripts/
│   ├── train_model.py        # Train IDS ML model
│   ├── detect_intrusions.py  # ML model inference & live traffic analysis
│   ├── replay_traffic.sh     # Tcpreplay script for simulating attacks
│   ├── send_alert.py         # Alerting mechanism for detected threats
│── dashboard/
│   ├── app.py                # Dash web application for monitoring
│── docker/
│   ├── Dockerfile            # Docker setup for IDS deployment
│   ├── docker-compose.yml    # Container orchestration
│── models/
│   ├── ids_model.h5          # Trained IDS model
│── logs/
│   ├── detection.log         # Log file for IDS alerts
│── requirements.txt          # Python dependencies
│── README.md                 # Documentation (This file)
```

---

## 1️⃣ Setup Ubuntu VM (Self-Hosted Runner)
### Step 1: Install Required Packages
SSH into the **Ubuntu VM (192.168.0.119)** and install dependencies:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl tar docker.io mongodb tcpreplay python3-pip
```

Enable and start MongoDB:

```bash
sudo systemctl enable --now mongodb
```

---

## 2️⃣ Configure GitHub Actions Self-Hosted Runner
### Step 2: Set Up Self-Hosted Runner
1. Navigate to **GitHub → Repository → Settings → Actions → Runners**.
2. Click **New self-hosted runner**, choose **Linux**, and follow the installation steps:

```bash
mkdir -p ~/actions-runner && cd ~/actions-runner
curl -o actions-runner-linux-x64.tar.gz -L https://github.com/actions/runner/releases/download/v2.XYZ/actions-runner-linux-x64-2.XYZ.tar.gz
tar xzf actions-runner-linux-x64.tar.gz
./config.sh --url https://github.com/lskengineer/cicids-automation --token YOUR_TOKEN
sudo ./svc.sh install && sudo ./svc.sh start
```

Verify the runner is active:

```bash
cd ~/actions-runner
./run.sh
```

---

## 3️⃣ Create GitHub Actions Workflow
Create `.github/workflows/deploy-ids.yml`:

```yaml
name: Deploy IDS

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: self-hosted
    steps:
      - name: Check out repository
        uses: actions/checkout@v3

      - name: Install System Dependencies
        run: |
          sudo apt update
          sudo apt install -y docker.io mongodb tcpreplay python3-pip
          sudo systemctl enable --now mongodb

      - name: Install Python Dependencies
        run: |
          pip3 install --upgrade pip
          pip3 install -r requirements.txt

      - name: Deploy IDS using Docker
        run: |
          cd docker
          docker-compose up -d --build

      - name: Start Traffic Replay
        run: |
          sudo tcpreplay --intf1=eth0 /home/ubuntu/pcaps/Wednesday-WorkingHours.pcap

      - name: Start Dashboard
        run: |
          cd dashboard
          python3 app.py
```

---

## 4️⃣ Docker Configuration for Deployment
### Step 1: Create Dockerfile
Create `docker/Dockerfile`:

```Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "detect_intrusions.py"]
```

### Step 2: Create Docker Compose Configuration
Create `docker/docker-compose.yml`:

```yaml
version: '3'
services:
  ids-app:
    build: .
    container_name: ids_model
    restart: always
    environment:
      - MONGO_URI=mongodb://mongodb:27017
    ports:
      - "8050:8050"

  mongodb:
    image: mongo
    container_name: mongodb
    restart: always
    ports:
      - "27017:27017"
```

---

## 5️⃣ Running the IDS Model & Live Traffic Simulation
### Step 1: Train IDS Model (Optional)
Create `scripts/train_model.py`:

```python
import joblib
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential([
    Dense(16, activation='relu', input_shape=(10,)),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.save("../models/ids_model.h5")
```

### Step 2: IDS Detection Script
Create `scripts/detect_intrusions.py`:

```python
import pymongo
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("../models/ids_model.h5")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ids_logs"]
alerts = db["alerts"]

def classify_traffic(features):
    prediction = model.predict(np.array([features]))[0]
    return "Malicious" if prediction > 0.5 else "Benign"

def log_alert(features):
    alert_data = {"features": features, "prediction": classify_traffic(features)}
    alerts.insert_one(alert_data)
    print(f"Alert Logged: {alert_data}")

log_alert([0.2, 0.5, 0.1, 0.9])
```

---

## 6️⃣ Real-Time Monitoring Dashboard
### Step 1: Create Dash Web App
Create `dashboard/app.py`:

```python
import dash
from dash import dcc, html
import pymongo
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ids_logs"]
alerts = db["alerts"]

app.layout = html.Div([
    html.H2("Live IDS Dashboard"),
    html.Div(id="alert-log"),
    dcc.Interval(id="interval-component", interval=2000, n_intervals=0)
])

@app.callback(Output("alert-log", "children"), Input("interval-component", "n_intervals"))
def update_log(n):
    latest_alerts = list(alerts.find().sort("_id", -1).limit(5))
    return html.Ul([html.Li(f"{alert['features']} - {alert['prediction']}") for alert in latest_alerts])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
```

---

## 7️⃣ Deployment and Testing
### Step 1: Deploy Using GitHub Actions
Push changes to GitHub:

```bash
git add .
git commit -m "Automated IDS Deployment"
git push origin main
```

### Step 2: Monitor IDS Logs
Check MongoDB logs:

```bash
mongo --eval 'db.ids_logs.alerts.find().pretty()'
```

### Step 3: View Real-Time Dashboard
Access **Dash UI** at:  
`http://192.168.0.119:8050`

---

✅ **The IDS system is now fully automated!**
