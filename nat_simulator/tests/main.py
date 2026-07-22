"""
Behavioural tests for the router. Run with:

    python3 -m nat_simulator.tests.main
"""
from ..defs import *
from ..delta import Delta
from ..ring_int import RingInt
from ..router import Router

WAN = WanIP("2.2.2.2")

# Two ports on one host, plus a second host.
DEST_A = AddrKey("8.8.8.8", 53)
DEST_A_ALT = AddrKey("8.8.8.8", 5000)
DEST_B = AddrKey("1.1.1.1", 53)


def router(nat_type, delta_type, **kwargs):
    return Router(WAN, nat_type, Delta(delta_type, **kwargs))


# 1. Endpoint independent: one mapping per internal endpoint,
#    reused no matter which destination is contacted.
def test_endpoint_independent_reuse():
    r = router("full_cone", "independent", step=1)
    src = AddrKey("10.0.1.50", 1024)

    first = r.connect(IP4, UDP, src, DEST_A)
    second = r.connect(IP4, UDP, src, DEST_B)
    assert first == second, (first, second)

    # A different source port is a different endpoint.
    other = r.connect(IP4, UDP, AddrKey("10.0.1.50", 1025), DEST_A)
    assert other != first, (other, first)

    # Both destinations were whitelisted against the one mapping.
    info = r.mappings[MappingKey(IP4, UDP, first)]
    assert {DEST_A, DEST_B} <= info.dests, info.dests
    assert info.src == src, info.src


# 2. Endpoint dependent: a new destination gets a new mapping.
def test_endpoint_dependent_mapping():
    r = router("symmetric", "independent", step=1)
    src = AddrKey("10.0.1.50", 1024)

    to_a = r.connect(IP4, UDP, src, DEST_A)
    to_b = r.connect(IP4, UDP, src, DEST_B)
    assert to_a != to_b, (to_a, to_b)

    # Port matters too (address and port dependent).
    to_a_alt = r.connect(IP4, UDP, src, DEST_A_ALT)
    assert to_a_alt not in (to_a, to_b)

    # Same flow twice is still the same mapping.
    assert r.connect(IP4, UDP, src, DEST_A) == to_a


# 3. An external port is never handed to two internal endpoints.
#    "equal" maps external port = source port, so distinct hosts
#    sharing a source port are guaranteed to collide.
def test_no_double_allocation():
    r = router("full_cone", "equal")

    mappings = []
    for host in range(0, 5):
        for port in range(1024, 1034):
            src = AddrKey("10.0.1.%d" % host, port)
            mappings.append(r.connect(IP4, UDP, src, DEST_A))

    assert len(set(mappings)) == len(mappings), "external port reused"
    assert len(r.mappings) == len(mappings), len(r.mappings)

    # Every port resolves back to the endpoint that owns it.
    for mapping in mappings:
        info = r.mappings[MappingKey(IP4, UDP, mapping)]
        assert info.mapping == mapping


# 4. Probing for a free port must not burn delta state.
def test_delta_not_burned_by_probing():
    r = router("full_cone", "independent", step=1)

    mappings = []
    for port in range(1024, 1044):
        mappings.append(r.connect(IP4, UDP, AddrKey("10.0.1.50", port), DEST_A))

    expected = list(range(mappings[0], mappings[0] + len(mappings)))
    assert mappings == expected, mappings


# 5. Inbound filtering, keyed only on what an inbound packet knows.
def test_filtering_matrix():
    # (same dest, same IP + new port, new IP, unmapped port)
    expected = {
        "full_cone": (True, True, True, False),
        "restrict": (True, True, False, False),
        "restrict_port": (True, False, False, False),
        "symmetric": (True, False, False, False),
        "open_internet": (True, True, True, True),
        "blocked": (False, False, False, False),
    }

    for nat_type, want in expected.items():
        r = router(nat_type, "independent", step=1)
        src = AddrKey("10.0.1.50", 1024)
        mapping = r.connect(IP4, UDP, src, DEST_A)

        got = (
            r.accept(IP4, UDP, mapping, DEST_A),
            r.accept(IP4, UDP, mapping, DEST_A_ALT),
            r.accept(IP4, UDP, mapping, DEST_B),
            r.accept(IP4, UDP, mapping + 1000, DEST_A),
        )

        assert got == want, (nat_type, got, want)


# 6. Port preserving NATs map straight through, ring or no ring.
def test_port_preserving():
    r = router("full_cone", "equal")
    assert r.connect(IP4, UDP, AddrKey("10.0.1.50", 80), DEST_A) == 80


# 7. A full router reports exhaustion.
def test_exhaustion():
    ring = RingInt(1024, 1028, 0)
    r = router("full_cone", "independent", step=1, delta_ring=ring)

    got = set()
    for port in range(0, ring.width):
        src = AddrKey("10.0.1.50", 1024 + port)
        got.add(r.connect(IP4, UDP, src, DEST_A))

    assert got == {1024, 1025, 1026, 1027}, got

    try:
        r.connect(IP4, UDP, AddrKey("10.0.1.50", 9999), DEST_A)
    except ValueError as e:
        assert "No mappings left" in str(e), e
    else:
        raise AssertionError("expected exhaustion")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print("ok", test.__name__)

    print("%d passed" % len(tests))
