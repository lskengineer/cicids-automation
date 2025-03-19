#!/bin/bash
echo "í´§ Configuring Zeek..."

# Install Zeek if not already installed
sudo apt install -y zeek

# Update Zeek's configuration for monitoring network interfaces
sudo zeekctl deploy

echo "âœ… Zeek configured and deployed!"

