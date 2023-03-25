from auth_peer import AuthPeer

def test_auth():
    print("hello world")
    auth_peer = AuthPeer(("192.168.1.66", 1234))
    auth_peer.authenticate_peer()

