from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import base64

# -------------------------
# Challenge 1: Base64 Maze
# -------------------------
class C1Protocol(Protocol):
    FLAG = "CTF_TWH3{b45364_d0ubl3}"

    def connectionMade(self):
        # send a double-base64 encoded flag
        once = base64.b64encode(self.FLAG.encode()).decode()
        twice = base64.b64encode(once.encode()).decode()
        msg = (
            "Welcome!\n"
            "Decode the following string to obtain the flag.\n"
            f"{twice.encode().hex()}\n"
            "Send the decoded flag followed by newline.\n"
        )
        self.transport.write(msg.encode())

    def dataReceived(self, data):
        attempt = data.strip().decode(errors="ignore")

        peer = self.transport.getPeer()
        client_ip = peer.host
        client_port = peer.port
        print(f"[+] Datos recibidos de {client_ip}:{client_port} -> {attempt}", flush=True)

        if attempt == self.FLAG:
            self.transport.write(b"Correct! Here is your flag: ")
            self.transport.write(self.FLAG.encode() + b"\n")
            self.transport.loseConnection()
        else:
            self.transport.write(b"Incorrect. Try again.\n")

# -------------------------
# Reactor setup
# -------------------------
if __name__ == '__main__':
    factories = [
        (9001, Factory.forProtocol(C1Protocol)),
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] Twisted CTF challenges running. Connect with `nc 127.0.0.1 <port>`")
    reactor.run()
