from lib.auth_peer import AuthPeer


def test_auth():
    auth_peer = AuthPeer("auth peer", ("192.168.1.66", 4702),3)
    print(auth_peer)
    auth_peer.authenticate_peers()
