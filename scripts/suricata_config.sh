#!/bin/bash
echo "í´§ Configuring Suricata for JSON output..."

# Install Suricata if not already installed
sudo apt install -y suricata

# Configure Suricata to output JSON logs
sudo sed -i 's/^#output eve-log:/output eve-log:/' /etc/suricata/suricata.yaml
sudo sed -i 's/^  # enabled: no/  enabled: yes/' /etc/suricata/suricata.yaml
sudo sed -i 's/^  filename: eve.json/  filename: \/var\/log\/suricata\/eve.json/' /etc/suricata/suricata.yaml
sudo systemctl restart suricata

echo "âœ… Suricata configured to log in JSON format!"

