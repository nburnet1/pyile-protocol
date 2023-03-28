from lib.peers.JoinPeer import JoinPeer
from random import randint


def test_peer():
    # peer
    # peer = JoinPeer("peer",("192.168.1.65", 4702+randint(0, 20)))
    peer = JoinPeer("peer", ("172.20.100.99", 4702 + randint(0, 20)))
    print(peer)
    # initial peer
    authenticated = peer.get_authenticated(("172.20.100.39", 4702), "password")
    # authenticated = peer.get_authenticated(("192.168.1.66", 4702), "password")
