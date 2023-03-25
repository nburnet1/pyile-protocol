from peer import Peer


def test_peer():
    peer = Peer(("192.168.1.65", 1234))
    print(peer.address)
    peer.authenticate(("192.168.1.66", 1234))
