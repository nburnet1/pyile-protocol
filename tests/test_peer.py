from lib.peer import Peer


def test_peer():
    # peer
    peer = Peer("peer",("192.168.1.65", 4702))
    print(peer)
    # initial peer
    peer.get_authenticated(("192.168.1.66", 4702))
