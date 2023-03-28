import pickle
import socket
import threading
from lib.error import *

class Peer:
    """

    """

    def __init__(self, username, address):
        if type(self) == Peer:
            raise TypeError("Peer cannot be directly instantiated")

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

    def broadcast(self):
        return

    def send(self):
        return

    def leave(self):
        return
