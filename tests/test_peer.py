from lib.JoinPeer import JoinPeer
from random import randint

def test_peer():
    # peer
    # peer = Peer("peer",("192.168.1.65", 4702))
    peer = JoinPeer("peer", ("172.20.100.99", 4702+randint(0, 20)))
    print(peer)
    # initial peer
    authenticated = peer.get_authenticated(("172.20.100.39", 4702), "password")
