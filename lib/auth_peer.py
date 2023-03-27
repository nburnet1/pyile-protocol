from lib.peer import Peer
from lib.error import *


class AuthPeer(Peer):
    def __init__(self,username,address, password_attempts):
        Peer.__init__(self,username=username,address=address)
        self.password_attempts = password_attempts
        self.master_set = []

    def authenticate_peers(self):
        self.socket.listen()
        addr, acc_connect = self.socket.accept()
        print("Got connection from", addr.getpeername())

        try:
            response = self.socket.accept()
            print(response.decode(self.BUFFER))
        except AuthenticationException("Could not accept response"):
            self.socket.close()
