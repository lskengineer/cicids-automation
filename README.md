#  CICIDS Automation Project

This **README** provides step-by-step instructions to **set up, deploy, and automate** the **CICIDS Automation Project** using **Dash for visualization** and **Dash for interactive AI model explanations**.

##  Project Overview

The **CICIDS Automation Project** is an **Intrusion Detection System (IDS) pipeline** that:
- **Simulates network traffic** from preprocessed dataset files.
- **Detects anomalies** using an AI model.
- **Logs detected anomalies** into **MongoDB**.
- **Provides dashboards** using **Dash** (`http://192.168.0.119:3001`).
- **Deploys an interactive AI explanation web app** using **Dash**.

##  1. Prerequisites

Ensure you have the following installed:

1. **Docker & Docker Compose**
   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose
   ```
2. **MongoDB**
   ```bash
   sudo apt install -y mongodb-org
   sudo systemctl start mongod
   sudo systemctl enable mongod
   ```
3. **Python & Virtual Environment**
   ```bash
   sudo apt install -y python3-pip python3-venv
   ```

##  2. Clone the Repository

```bash
git clone https://github.com/your-username/cicids-automation.git
cd cicids-automation
```

##  3. Manual Deployment

### **Step 3.1: Set Up Dependencies**

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### **Step 3.2: Preprocess Dataset**

```bash
source cicids_env/bin/activate
python3 scripts/preprocess_csv.py
deactivate
```

### **Step 3.3: Train AI Model**

```bash
source cicids_env/bin/activate
python3 scripts/train_ai_model.py
deactivate
```

### **Step 3.4: Convert Data to PCAP for Simulation**

```bash
source cicids_env/bin/activate
python3 scripts/csv_to_pcap.py
deactivate
```

### **Step 3.5: Simulate Network Traffic**

```bash
chmod +x scripts/simulate_traffic.sh
./scripts/simulate_traffic.sh
```

### **Step 3.6: Insert IDS Logs into MongoDB**

```bash
python3 scripts/insert_logs_mongodb.py
```

### **Step 3.7: Deploy Dash with Docker**

```bash
mkdir -p ~/cicids-automation/Dash
cd ~/cicids-automation/Dash
cat <<EOF > docker-compose.yml
version: '3'
services:
  Dash:
    image: Dash/Dash
    container_name: Dash
    restart: always
    ports:
      - "3001:3000"
    environment:
      MB_DB_TYPE: postgres
      MB_DB_DBNAME: Dash
      MB_DB_PORT: 5432
      MB_DB_USER: Dash_user
      MB_DB_PASS: Dash_password
      MB_DB_HOST: 192.168.0.119
    volumes:
      - ./Dash-data:/Dash-data
EOF
docker-compose up -d
```

 **Dash will be available at:** `http://192.168.0.119:3001`

### **Step 3.8: Deploy Dash Web Application**

```bash
source cicids_env/bin/activate
python3 scripts/deploy_dash.py
deactivate
```

 **Dash Web App will be deployed!**

##  4. Automate with GitHub Actions

### **Step 4.1: Push the Changes**

```bash
git add .
git commit -m "Updated project with Dash visualization using Docker"
git push origin main
```

 **GitHub Actions will now automatically deploy Dash and Dash.**

##  5. Monitoring

### **Monitor GitHub Actions Workflow**

1. Go to [GitHub → Repository → Actions](https://github.com/your-username/cicids-automation/actions).
2. Check if all **jobs** complete successfully.

### **Monitor Docker Containers**

To see running Dash and Dash containers:

```bash
docker ps
```

To check logs for Dash:

```bash
docker logs Dash
```

##  6. Accessing the Applications

| Application | URL |
|-------------|-------------|
| **Dash Web Application** | `http://192.168.0.119:3001` |
| **Dash Web Application** | `http://YOUR-SERVER-IP:DASH-PORT` |

##  7. Summary

 **Dash (`192.168.0.119:3001`) for IDS visualization**  
 **Dash Web App for AI Model Insights**  
 **Automated deployment via GitHub Actions**  
 **MongoDB for IDS log storage**  

 **Your CICIDS project is now fully automated with real-time visualization!** 

