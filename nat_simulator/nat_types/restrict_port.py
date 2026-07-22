"""
Restrict type nat = seen dest ip and reply port must match.
"""
def plugin(router, src, dest, flow):
    if not flow:
        return False
    
    if src != flow.src:
        return False
    
    # Address-dependent filtering (IP and port.)
    if dest != flow.dest:
        return False
    
    return True