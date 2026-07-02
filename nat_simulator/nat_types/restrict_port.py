"""
Restrict type nat = seen dest ip and reply port must match.
"""
def plugin(router, src, dest, flow):
    if not flow:
        return False
    
    if src != flow.src:
        return False
    
    # Previously seen dest -- endpoint independent.
    if dest not in router.dest_whitelist:
        return False
    
    return True