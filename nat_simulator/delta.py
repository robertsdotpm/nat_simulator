from .defs import *
from .utils import *
from .ring_int import *

class Delta:
    def __init__(self, delta_type, step=1, delta_extra=None, delta_ring=None):
        self.plugin = load_plugin(("delta_types", delta_type))
        self.ring = delta_ring or RingInt(1024, MAX_PORT, 0)
        self.extra = delta_extra or {}
        self.step = step
        self.value = self.ring

    def allocate(self, flow):
        return self.plugin(self, flow)
    