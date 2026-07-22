"""
1. Reuse mapping on same src ip:port.
2. Filtering = same dest IP
    Reply port can be anything.
"""
def plugin(router, dest, mapping_info):
    if mapping_info is None:
        return False

    # Address-dependent filtering (IP only.)
    if dest.ip not in mapping_info.dests:
        return False

    return True