#!/bin/bash
INTERFACE="enp0s3"
echo "Replaying traffic on interface: $INTERFACE"
sudo tcpreplay --intf1=$INTERFACE data/ids_data.pcap
echo "✅ Traffic simulation completed!"

