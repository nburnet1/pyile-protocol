import pickle
import random
import socket
import threading

from lib.peers.Peer import Peer
from lib.error import *


class JoinPeer(Peer):
    def __init__(self, username, address):
        Peer.__init__(self, username=username, address=address)
        self.auth_peer = None



    def get_authenticated(self, starting_address, password):
        """
        The first method that should be called when a peer is created.
        :param starting_address: tuple of (ip, port)
        :param password: string
        :return: True if authenticated, False if not
        """

        def password_check():
            """
            Helper function that checks the password.
            :return: boolean True if authenticated, False if not
            """
            try:
                self.auth_socket.send(password.encode(self.ENCODE))
                pw_status = self.auth_socket.recv(self.BUFFER).decode(self.ENCODE)
                if pw_status == "authenticated":
                    print(str(password) + " is correct")
                    # adding auth peer
                    self.auth_peer = starting_address
                    # sends new socket to auth peer
                    pickled_socket = pickle.dumps(self.peer_address)
                    self.auth_socket.send(pickled_socket)
                    # receives peers from auth peer
                    recv_peers = self.auth_socket.recv(self.BUFFER)
                    self.peers = pickle.loads(recv_peers)
                    print("Received peers from auth: ", self.peers)
                    return True
                elif pw_status == "notauthenticated":
                    raise AuthenticationException("Password is incorrect")
            except AuthenticationException as e:
                print(e)
                return False



        # Connect to initial peer
        try:
            self.auth_socket.connect(starting_address)
        except ConnectionRefusedError:
            self.auth_socket.close()

        # Receive banned status from initial peer
        try:
            banned = self.auth_socket.recv(self.BUFFER).decode(self.ENCODE)
            print(banned)
            if banned == "banned":
                raise AuthenticationException("You are banned from this network")
        except AuthenticationException as e:
            print(e)
            self.auth_socket.close()
            return

        # Performs password check
        authenticated = password_check()
        if authenticated:
            self.join_beat()

    def join_beat(self):
        try:
            self.auth_socket.settimeout(10)
            beat = self.auth_socket.recv(self.BUFFER).decode(self.ENCODE)
            print("Heart beat received")
            if not beat:
                raise Exception("Server Disconnect")

            self.auth_socket.send("heartbeat".encode(self.ENCODE))
        except Exception as e:
            print(e)
            self.auth_socket.close()
            return

        threading.Timer(5, self.join_beat).start()
