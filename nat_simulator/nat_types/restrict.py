"""
Restrict type nat = seen dest IP. Reply port can be anything.
"""
def plugin(router, src, dest, flow):
    if not flow:
        return False
    
    if src != flow.src:
        return False
    
    # Previously seen dest -- endpoint independent.
    if dest.ip not in router.dest_whitelist:
        return False
    
    return True