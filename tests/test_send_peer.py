import sys
import threading

from lib.peers.JoinPeer import JoinPeer
from lib import utils
from random import randint


def test_peer():

    peer = JoinPeer(("192.168.1.65", 4702+randint(0, 20)))
    #peer = JoinPeer(("172.20.100.99", 4702 + randint(0, 20)))

    #authenticated = peer.get_authenticated(("172.20.100.39", 4702), "password")
    authenticated = peer.get_authenticated(("192.168.1.66", 4702), "password")


    try:
        connect_thread = threading.Thread(target=peer.connect)
        connect_thread.start()
    except:
        print("threads terminated")

    while not peer.disconnected:
        data = input("~: ")
        if data == "exit":
            peer.auth_socket.close()
            peer.peer_socket.close()
            peer.disconnected = True
            peer.threads.append(connect_thread)
            utils.join_threads(peer.threads)

        elif data == "peers":
            print(peer.peers)
        else:
            peer.broadcast(data)
