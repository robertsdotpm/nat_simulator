"""
1. Reuse mapping on same src ip:port.
2. Filtering: seen dest ip and reply port must match.
"""
def plugin(router, dest, mapping_info):
    if mapping_info is None:
        return False

    # Address-dependent filtering (IP and port.)
    if dest not in mapping_info.dests:
        return False

    return True