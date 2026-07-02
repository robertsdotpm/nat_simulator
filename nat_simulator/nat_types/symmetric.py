def plugin(router, src, dest, flow):
    if not flow:
        return False
    
    if src != flow.src:
        return False
    
    # Mappings are tied to endpoints.
    if dest != flow.dest:
        return False

    return True