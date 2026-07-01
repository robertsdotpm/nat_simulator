from dataclasses import dataclass
import socket

# No NAT at all.
OPEN_INTERNET = 1

# There is no NAT but there is some kind of firewall.
SYMMETRIC_UDP_FIREWALL = 2

# Mappings are made for local endpoints.
# Then any destination can use the mapping to reach the local enpoint.
# Note: May be incorrectly detected if using TCP.
FULL_CONE = 3

# NAT reuses mapping if same src ip and port is used.
# Destination must be white listed. It can use any port to send replies on.
# Endpoint-independent
# Note: May be incorrectly detected if using TCP.
RESTRICT_NAT = 4

# Mappings reused based on src ip and port.
# Destination must be white listed and use the port requested by recipient.
# Endpoint-independent (with some limitations.)
# Note: May be incorrectly detected if using TCP.
RESTRICT_PORT_NAT = 5

# Different mapping based on outgoing hosts.
# Even if same source IP and port reused.
# AKA: End-point dependent mapping.
SYMMETRIC_NAT = 6

# No response at all.
BLOCKED_NAT = 7

IP4 = socket.AF_INET
IP6 = socket.AF_INET6
UDP = socket.SOCK_DGRAM
TCP = socket.SOCK_STREAM

@dataclass(frozen=True, slots=True)
class FlowKey:
    af: int
    proto: int
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int