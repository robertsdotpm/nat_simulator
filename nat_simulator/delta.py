from .defs import *
from .utils import *

class Delta:
    def __init__(self, delta_type, delta_extra=None):
        self.delta_extra = delta_extra
        self.delta_plugin = load_plugin(("delta_types", delta_type))
        self.value = 1 # start at mapping 1

    def allocate(self):
        return self.delta_plugin(self, self.delta_extra)
    