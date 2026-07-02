"""
A full cone NAT lets any destination connect back providing an existing
mapping exists.
"""
def plugin(router, src, dest, flow): 
    if not flow:
        return False
    
    if src != flow.src:
        return False

    return True