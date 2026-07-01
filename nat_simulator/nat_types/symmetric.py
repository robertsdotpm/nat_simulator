def plugin(router, af, proto, src, dest, mapping):
    flow_key = (af, proto, mapping)
    if flow_key not in router.flows:
        return False
    
    flow = router.flows[flow_key]
    if src[0] != flow.src_ip:
        return False
    
    if src[1] != flow.src_port:
        return False
    
    # Mappings are tied to endpoints.
    if dest[0] != flow.dest_ip:
        return False
    if dest[1] != flow.dest_port:
        return False

    return True