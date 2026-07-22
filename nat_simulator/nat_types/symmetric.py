"""
1. Mappings different for every unique quad tuple.
    i.e. even if reusing (af, proto, src ip, src port)
    mapping will be different
2. 
"""
def plugin(router, dest, mapping_info):
    if mapping_info is None:
        return False

    # Mappings are tied to endpoints.
    if dest not in mapping_info.dests:
        return False

    return True