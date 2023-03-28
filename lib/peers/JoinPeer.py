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
                self.socket.send(password.encode(self.ENCODE))
                pw_status = self.socket.recv(self.BUFFER).decode(self.ENCODE)
                if pw_status == "authenticated":
                    print(str(password) + " is correct")
                    self.auth_peer
                    return True
                elif pw_status == "notauthenticated":
                    raise AuthenticationException("Password is incorrect")
                    return False
            except AuthenticationException as e:
                print(e)
                self.socket.close()

        # Connect to initial peer
        try:
            self.socket.connect(starting_address)
        except ConnectionRefusedError:
            self.socket.close()

        # Receive banned status from initial peer
        try:
            banned = self.socket.recv(self.BUFFER).decode(self.ENCODE)
            print(banned)
            if banned == "banned":
                raise AuthenticationException("You are banned from this community")
        except AuthenticationException as e:
            print(e)
            self.socket.close()
            return

        # Performs password check
        return password_check()
