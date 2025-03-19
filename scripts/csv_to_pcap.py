import pandas as pd
from scapy.all import IP, TCP, Ether, wrpcap, conf
import warnings

# Suppress Scapy warnings about MAC addresses
conf.verb = 0  # Set verbosity to 0 (no output)
warnings.filterwarnings("ignore", category=UserWarning, module="scapy")

# Load the CSV file
df = pd.read_csv("data/ids_data_combined.csv")

# Define the output PCAP file path
pcap_file = "data/ids_data.pcap"

# Create a list to store packets
packets = []

# Iterate through each row to create packets using 'src_ip' and 'dst_ip'
for _, row in df.iterrows():
    pkt = Ether() / IP(src=row["src_ip"], dst=row["dst_ip"]) / TCP()  # Using correct column names
    packets.append(pkt)

# Write the packets to a PCAP file
wrpcap(pcap_file, packets)

print(f"✅ PCAP file created: {pcap_file}")

