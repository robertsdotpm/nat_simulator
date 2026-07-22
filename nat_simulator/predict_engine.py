from .defs import *
from .router import Router
from .delta import Delta

class PredictEngine:
    def __init__(self, src_router, dest_router):
        self.src_router = src_router
        self.dest_router = dest_router

    # Predict dest mappings.
    def predict(self, af, proto, n):
        mappings = []
        for i in range(0, n):
            src = AddrKey(self.src_router.wan_ip.get(af), i)
            dest = AddrKey(self.dest_router.wan_ip.get(af), i)

            mapping = self.dest_router.get_mapping(af, proto, src, dest)
            mappings.append(mapping)

        return mappings

src_router = Router(
    WanIP("2.2.2.2"),
    "full_cone", 
    Delta("independent", step=2)
)

dest_router = Router(
    WanIP("4.4.4.4"),
    "full_cone", 
    Delta("independent", step=1)
)

engine = PredictEngine(src_router, dest_router)
print(engine.predict(
    IP4, TCP, 4
))

"""
    original:
    - includes our and their mappings
    - has best guest for what 

    - could algorithm work for collisons?
    - 

    - proto:
        - get our mappings -> them
            - with assumed their mappings
        - update best guess if they return


"""