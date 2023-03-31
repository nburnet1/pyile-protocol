import sys
import threading

from lib.peers.AuthPeer import AuthPeer
from lib.peers.JoinPeer import JoinPeer
from lib import utils


def test_auth():
    auth_peer = AuthPeer(("192.168.1.66", 4702), 1, "password")
    # auth_peer = AuthPeer(("172.20.100.39", 4702), 1, "password")
    print(auth_peer)

    auth_thread = threading.Thread(target=auth_peer.authenticate_peers)
    peer_thread = threading.Thread(target=auth_peer.connect)
    auth_thread.start()
    peer_thread.start()

    while not auth_peer.disconnected:
        data = input("~: ")
        if data == "exit":
            auth_peer.auth_socket.close()
            auth_peer.peer_socket.close()
            auth_peer.disconnected = True
            auth_peer.threads.append(auth_thread)
            auth_peer.threads.append(peer_thread)
            utils.join_threads(auth_peer.threads)

        elif data == "peers":
            print(auth_peer.peers)
        else:
            auth_peer.broadcast(data)
