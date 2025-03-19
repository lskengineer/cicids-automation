#!/bin/bash
echo "� Configuring Zeek..."

# Install Zeek if not already installed
sudo apt install -y zeek

# Update Zeek's configuration for monitoring network interfaces
sudo zeekctl deploy

echo "✅ Zeek configured and deployed!"

