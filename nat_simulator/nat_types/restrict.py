"""
Restrict type nat = seen dest IP. Reply port can be anything.
"""
def plugin(router, src, dest, flow):
    if not flow:
        return False
    
    if src != flow.src:
        return False
    
    # Address-dependent filtering (IP only.)
    if dest.ip != flow.dest.ip:
        return False
    
    return True