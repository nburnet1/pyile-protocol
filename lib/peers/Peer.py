import pickle
import random
import socket
import threading
import time

from lib.error import *


class Peer:
    """

    """

    def __init__(self, address):
        if type(self) == Peer:
            raise TypeError("Peer cannot be directly instantiated")

        self.ENCODE = 'utf-8'
        self.BUFFER = 2048
        self.disconnected = False
        self.address = address
        self.auth_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.auth_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.auth_socket.bind(self.address)

        self.peer_address =(self.address[0], 49000 + random.randint(0, 1000))
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_socket.bind(self.peer_address)

        self.peers = []

    def __str__(self):
        return f"Peer at {self.address}"

    def handle_peer(self, addr):
        data = addr.recv(self.BUFFER).decode(self.ENCODE)
        print(data)
        addr.send(data.encode(self.ENCODE))

    def connect(self):
        self.peer_socket.listen()
        # print("Listening for connections...")
        while not self.disconnected:
            addr, acc_connect = self.peer_socket.accept()
            self.handle_peer(addr)

    def broadcast(self, msg):
        for peer in self.peers:
            if peer != self.peer_address:
                self.send(peer, msg)

    def send(self, address, msg):
        if address == self.peer_address:
            print("Cannot send to self")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
            send_sock.settimeout(1)
            try:
                send_sock.connect(address)
                # print("sending: ", msg, "to", address)
                send_sock.send(msg.encode(self.ENCODE))
                data = send_sock.recv(self.BUFFER).decode(self.ENCODE)
            except Exception:
                send_sock.close()
                print("Peer at", address, "is not responding")



    def leave(self):
        self.disconnected = True
