"""
Restrict type nat = seen dest IP. Reply port can be anything.
"""
def plugin(router, af, proto, src, dest, mapping):
    flow_key = (af, proto, mapping)
    if flow_key not in router.flows:
        return False
    
    flow = router.flows[flow_key]
    if src[0] != flow.src_ip:
        return False
    
    if src[1] != flow.src_port:
        return False
    
    # Previously seen dest -- endpoint independent.
    if dest[0] not in router.dests:
        return False
    
    return True