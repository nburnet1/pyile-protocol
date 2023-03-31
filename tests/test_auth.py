import threading

from lib.peers.AuthPeer import AuthPeer


def test_auth():
    auth_peer = AuthPeer(("192.168.1.66", 4702), 1, "password")
    # auth_peer = AuthPeer(("172.20.100.39", 4702), 1, "password")
    print(auth_peer)
    try:
        auth_thread = threading.Thread(target=auth_peer.authenticate_peers)
        peer_thread = threading.Thread(target=auth_peer.connect)
        auth_thread.start()
        peer_thread.start()
    except:
        print("threads terminated")

    while True:
        data = input("What do you want to send: ")
        if data == "exit":
            auth_peer.auth_socket.close()
            auth_peer.peer_socket.close()
            peer_thread.join()
            auth_peer.disconnected = True
            return
        elif data == "peers":
            print(auth_peer.peers)
        else:
            auth_peer.broadcast(data)

