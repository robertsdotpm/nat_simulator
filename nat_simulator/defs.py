from dataclasses import dataclass, field
import socket

MAX_PORT = 65535
IP4 = socket.AF_INET
IP6 = socket.AF_INET6
UDP = socket.SOCK_DGRAM
TCP = socket.SOCK_STREAM

@dataclass(frozen=True, slots=True)
class AddrKey:
    ip: str
    port: int

@dataclass(frozen=True, slots=True)
class FlowKey:
    af: int
    proto: int
    src: AddrKey
    dest: AddrKey

@dataclass(frozen=True, slots=True)
class ClientKey:
    af: int
    proto: int
    src: AddrKey

# The external port space -- what an inbound packet can key on.
@dataclass(frozen=True, slots=True)
class MappingKey:
    af: int
    proto: int
    mapping: int

@dataclass(slots=True)
class MappingInfo:
    src: AddrKey
    mapping: int
    dests: set = field(default_factory=set)

    # Filtering matches on dest IP (restrict) or IP and port
    # (restrict port / symmetric) so record both forms.
    def allow(self, dest):
        self.dests.add(dest)
        self.dests.add(dest.ip)

@dataclass(frozen=True, slots=True)
class WanIP:
    v4: str
    v6: str = None

    def get(self, af):
        if af == IP4:
            return self.v4
        
        if af == IP6:
            return self.v6
        
        raise Exception("unknown AF")