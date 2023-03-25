import pickle
import socket
import threading
"""
Peer class that has all functionalities for p2p messaging.

A peer can:
Connect
Authenticate
Broadcast
Send
Receive
Leave
"""


class Peer:
    def __init__(self, address):
        self.address = address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.peers = set()

    def connect(self):
        return

    def authenticate(self, starting_address):
        self.socket.connect(starting_address)
        self.socket.close()


    def broadcast(self):
        return

    def send(self):
        return

    def leave(self):
        return
