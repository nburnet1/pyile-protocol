import threading

from lib.peers.JoinPeer import JoinPeer
from random import randint


def test_peer():
    # peer
    # peer = JoinPeer(("192.168.1.65", 4702+randint(0, 20)))
    peer = JoinPeer(("172.20.100.99", 4702 + randint(0, 20)))
    # print(peer)
    # initial peer
    authenticated = peer.get_authenticated(("172.20.100.39", 4702), "password")
    # authenticated = peer.get_authenticated(("192.168.1.66", 4702), "password")
    # print(peer)
    # address = input("Enter address:")
    # port = input("Enter port: ")
    # tup_address = (address, int(port))
    try:
        connect_thread = threading.Thread(target=peer.connect)
        connect_thread.start()
    except:
        print("threads terminated")

    while True:
        data = input("What do you want to send: ")
        if data == "exit":
            peer.auth_socket.close()
            peer.peer_socket.close()
            connect_thread.join()
            peer.disconnected = True
            return
        elif data == "peers":
            print(peer.peers)
        else:
            peer.broadcast(data)
