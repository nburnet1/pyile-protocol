import pickle

from lib.peers.Peer import Peer
from lib.error import *


class AuthPeer(Peer):
    """
    A class to represent an authenticating peer.
    This class inherits from the Peer class.
    ...

    Attributes
    ----------
    username : str
        username of the peer that others will see
    address : tuple of (ip, port)
        address of the authentication peer
    password_attempts : int
        Allowed attempts that a joining peer is allowed
    password : str
        Password that joining peers must authenticate with

    Methods
    -------
    authenticate_peers()
        The first method that should be called when an authentication peer is created
    """

    def __init__(self, username, address, password_attempts, password):
        Peer.__init__(self, username=username, address=address)
        self.password_attempts = password_attempts
        self.peers.append(self.peer_address)
        self.blocked_peers = set()
        self.password = password

    def authenticate_peers(self):
        """
        The first method that should be called when an authentication peer is created
        :return:
        """

        def auth_password_check():
            """

            :return:
            """
            try:
                password = addr.recv(self.BUFFER).decode(self.ENCODE)
                print(password)
                if password == self.password:
                    # Sends authenticated status to peer
                    addr.send("authenticated".encode(self.ENCODE))
                    # Receives peer address from peer
                    peer_recv = addr.recv(self.BUFFER)
                    self.peers.append(pickle.loads(peer_recv))
                    # Sends new set to peer
                    addr.send(pickle.dumps(self.peers))
                    print(self.peers)
                    return
                else:
                    addr.send("notauthenticated".encode(self.ENCODE))
                    raise AuthenticationException("Incorrect password.")
            except AuthenticationException as e:
                print(e)
        self.auth_socket.listen()

        while True:
            addr, acc_connect = self.auth_socket.accept()
            print("Got connection from: ", addr.getpeername())
        #self.blocked_peers.add(addr.getpeername())  # Uncomment to test ban.
        # Checks if joining peer in banned
            if addr.getpeername() not in self.blocked_peers:
                # Sends not banned status to peer
                try:
                    addr.send("notbanned".encode(self.ENCODE))
                except AuthenticationException:
                    print("Could not send banned status to peer.")
                # Performs authentication
                auth_password_check()
            else:
                print(addr.getpeername(), "is banned")
                addr.send("banned".encode(self.ENCODE))
                addr.close()

