import threading
import time

from pyile_protocol.lib.peers.Peer import Peer
from pyile_protocol.lib.utils import *
from pyile_protocol.lib.error import *


class AuthPeer(Peer):
    """
    A class to represent an authenticating peer.
    This class inherits from the Peer class.
    ...

    Attributes
    ----------

    address : tuple of (ip, port)
        address of the authentication peer
    password_attempts : int
        Allowed attempts that a joining peer is allowed
    password : str
        Password that joining peers must authenticate with
    blocked_peers : set
        Set of peers that are banned from joining the network
    changes_made : bool
        Boolean to check if changes have been made to the network


    Methods
    -------
    __init__(address, password_attempts, password)
        Constructor for the AuthPeer class
    authenticate_peers()
        The first method that should be called when an authentication peer is created
    """

    def __init__(self, address, password_attempts, password):
        Peer.__init__(self, address=address)
        self.password_attempts = password_attempts
        self.peers.append(self.peer_address)
        self.blocked_peers = set()
        self.changes_made = False
        self.password = password
        self.connected_addrs = []
        self.dist_sockets = []

    def _auth_password_check(self, addr):
        """
            Auxiliary function to help authenticate
        :return: peer address if authenticated, None if not
        """
        try:
            password = addr.recv(self.BUFFER)
            password_json = recv_json(password)
            print(addr.getpeername(), "Trying to login with password:", password)
            if password_json["shadow"] == self.password:
                # Sends authenticated status to peer
                auth = send_json({"authenticated": True})
                addr.send(auth)
                # Receives peer address from peer
                peer_recv = addr.recv(self.BUFFER)
                peer_json = recv_json(peer_recv)
                peer_tuple = tuple(peer_json["peer address"])
                self.peers.append(peer_tuple)
                # Sends new set to peer
                print(self.peers)
                distro_json = send_json({"distro": self.peers})
                addr.send(distro_json)
                print(self.peers)
                return peer_tuple
            else:
                auth = send_json({"authenticated": False})
                addr.send(auth)
                raise AuthenticationException("Incorrect password.")
        except AuthenticationException as e:
            print(e)
            return None

    def authenticate_peers(self):
        """
        The first method that should be called when an authentication peer is created.
        Starts a thread to listen for incoming connections, Authenticates peers and calls the
        heartbeat method.
        """
        distribute_thread = threading.Thread(target=self.auth_distribute)
        self.dist_socket.listen()
        distribute_thread.start()
        self.auth_socket.listen()

        while not self.disconnected:
            try:
                addr, acc_connect = self.auth_socket.accept()
                print("Got connection from: ", addr.getpeername())

                # self.blocked_peers.add(addr.getpeername())  # Uncomment to test ban.
                # Checks if joining peer in banned
                if addr.getpeername() not in self.blocked_peers:
                    # Sends not banned status to peer
                    try:
                        banned = send_json({"banned": False})
                        print("Sent Banned status", banned)
                        addr.send(banned)

                    except AuthenticationException:
                        print("Could not send banned status to peer.")
                    # Performs authentication
                    peer_address = self._auth_password_check(addr)
                    if peer_address is not None:
                        addr.send(send_json({"dist addr": self.dist_address}))
                        print("DIST ADDRESS: ", self.dist_address)
                        dist_connected = self.dist_socket.accept()
                        self.dist_sockets.append(dist_connected)
                        print("Dist Sockets: ", self.dist_sockets)
                        self.connected_addrs.append(addr)
                        # print("dist addr: ", dist_addr)
                        auth_thread = threading.Thread(target=self.auth_beat, args=(addr, peer_address, dist_connected))

                        auth_thread.start()
                        self.changes_made = True

                else:
                    print(addr.getpeername(), "is banned")
                    banned = send_json({"banned": True})
                    addr.send(banned)
                    addr.close()
            except:
                pass

    def auth_beat(self, addr, peer_address, dist_addr):
        """
        Sends a heartbeat to the peer to check if it is still connected
        :return:
        """
        while not self.disconnected:
            try:
                addr.send(send_json({"<3": True}))
                beat = addr.recv(self.BUFFER)
                if not beat:
                    raise ConnectionResetError
            except ConnectionResetError:
                print("Peer disconnected: ", peer_address)
                self.peers.remove(peer_address)
                self.connected_addrs.remove(addr)
                self.dist_sockets.remove(dist_addr)
                print(self.peers)
                self.changes_made = True
                return
            time.sleep(2)

    def auth_distribute(self):
        while not self.disconnected:
            if self.changes_made and len(self.dist_sockets) > 0:
                print("changes made:", self.dist_sockets)
                for addr in self.dist_sockets:
                    print(addr)
                    distro_json = send_json({"distro": self.peers})
                    addr[0].send(distro_json)
                self.changes_made = False
