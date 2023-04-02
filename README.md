<h1 style="text-align:center;">Pyile Protocol Documentation:</h1>
<h2>Introduction:</h2>
<p>
This document describes the network protocol used by the pyile application over TCP/IP on port 4702. 
The protocol is used for communication and authentication between peers. 
</p>

<h2>Protocol Overview</h2>
<p>
The Pyile protocol is for 
</p>

<h3>Protocol Flow</h3>

* Authenticating peer is established listening on port 4702 for potential peers
* Authenticating peer, then generates a random port and begins to listen to already established peers. (Should only be themselves)
* A Joining peer then requests to be authenticated by the initial peer.
* The initial peer then checks if the peer is already banned and then checks the password.
* If the password is correct, then the peer is added and then given the list of peers that can be communicated with.
* A heartbeat is then established between both peers.
* The joining peer can now communicate in the network.

<h3>Special Flows</h3>


<img src="https://www.burnette.tech/img/Pyile.png"/>
<h5><i>Figure 1</i></h5>

<h3>Message Types</h3>

<h3>Error Handling</h3>
<p>
The protocol has custom exceptions to further the detail of errors.
</p>

<h3>Security</h3>
<p>
The protocol implements an authentication process equipped with a password check and banned status. There is
currently zero encryption.
</p>

<h2>Code Example</h2>

<h4>Authenticating Peer</h4>
```python
auth_peer = AuthPeer(address=("192.168.1.66", 4702), password_attempts=1, password="password")

auth_thread = threading.Thread(target=auth_peer.authenticate_peers)
peer_thread = threading.Thread(target=auth_peer.connect)
auth_thread.start()
peer_thread.start()

while not auth_peer.disconnected:
    data = input("~: ")
    if data == "exit":
        auth_peer.leave()
    elif data == "peers":
        print(auth_peer.peers)
    else:
        auth_peer.broadcast(data)
```
<h4>Peer</h4>
```python
peer = JoinPeer(address=("192.168.1.65", 4702))
peer.get_authenticated(("192.168.1.66", 4702), "password")


connect_thread = threading.Thread(target=peer.connect)
connect_thread.start()


while not peer.disconnected:
    data = input("~: ")
    if data == "exit":
        peer.leave()

    elif data == "peers":
        print(peer.peers)
    else:
        peer.broadcast(data)
```
