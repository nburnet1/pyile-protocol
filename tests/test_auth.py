from lib.AuthPeer import AuthPeer
import threading

def test_auth():
    # auth_peer = AuthPeer("auth peer", ("192.168.1.66", 4702),3)
    auth_peer = AuthPeer("auth peer", ("172.20.100.39", 4702), 1, "password")
    print(auth_peer)
    auth_peer.authenticate_peers()
    auth_peer.socket.close()
