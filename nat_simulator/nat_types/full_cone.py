"""
A full cone NAT lets any destination connect back providing an existing
mapping exists. Pretty simple, right.
"""
def approve(router, af, proto, mapping, dest):
    flow_key = (af, proto, mapping)
    if flow_key in router.flows:
        return True
    else:
        return False