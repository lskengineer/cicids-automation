#!/bin/bash
echo "í´§ Installing system dependencies..."

# Update & Install core tools
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git unzip wget python3-pip docker.io docker-compose tcpreplay

# Install MongoDB
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod

# Install IDS Tools
sudo apt install -y snort suricata zeek

# Install Python Virtual Environment
python3 -m venv cicids_env
source cicids_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

echo "âœ… Setup completed!"

