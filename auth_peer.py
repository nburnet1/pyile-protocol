from peer import Peer


class AuthPeer(Peer):
    def __init__(self,address):
        Peer.__init__(self,address=address)

    def authenticate_peer(self):
        self.socket.listen()
        addr, acc_connect = self.socket.accept()
        print("Got connection from", addr.getpeername())
        self.socket.close()
