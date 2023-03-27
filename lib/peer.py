import pickle
import socket
import threading
from lib.error import *

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

    def __init__(self, username, address):
        self.ENCODE = 'utf-8'
        self.BUFFER = 1024
        self.username = username
        self.address = address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.peers = set()

    def __str__(self):
        return f"{self.username} at {self.address}"

    def connect(self):
        return

    def get_authenticated(self, starting_address):
        """
        :param starting_address:
        :return:

        This method is used to authenticate a peer.
        """
        try:
            self.socket.connect(starting_address)
        except ConnectionRefusedError:
            self.socket.close()

        try:
            self.socket.send("Hello!".encode(self.ENCODE))
        except AuthenticationException("Could not be authenticated"):
            self.socket.close()

    def broadcast(self):
        return

    def send(self):
        return

    def leave(self):
        return
