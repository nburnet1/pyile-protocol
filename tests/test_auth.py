import threading

from lib.peers.AuthPeer import AuthPeer


def test_auth():
    auth_peer = AuthPeer("auth peer", ("192.168.1.66", 4702),1, "password")
    # auth_peer = AuthPeer("auth peer", ("172.20.100.39", 4702), 1, "password")
    print(auth_peer)
    auth_thread = threading.Thread(target=auth_peer.authenticate_peers)
    peer_thread = threading.Thread(target=auth_peer.connect)

    auth_thread.start()
    peer_thread.start()

