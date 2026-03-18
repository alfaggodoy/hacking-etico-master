from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import json

# -------------------------
# Challenge 9: JSON Access
# -------------------------
class C9Protocol(Protocol):
    FLAG = "CTF_TWH3{js0n_4dm1n}"

    def connectionMade(self):
        self.transport.write(b"Welcome to JSON Access!\n")
        self.transport.write(b"Send a JSON object saying that you are 'admin' and have access :)\n")

    def dataReceived(self,data):
        try:
            obj = json.loads(data.decode())

            peer = self.transport.getPeer()
            client_ip = peer.host
            client_port = peer.port
            print(f"[+] Datos recibidos de {client_ip}:{client_port} -> {data.decode()}", flush=True)

            if obj.get("username")=="admin" and obj.get("access") is True:
                self.transport.write(b"Correct! Flag: "+self.FLAG.encode()+b"\n")
                self.transport.loseConnection()
                return
        except Exception as e:
            self.transport.write(f"Error parsing JSON: {e}\n".encode())
            return
        self.transport.write(b"Invalid JSON or wrong fields.\n")

# -------------------------
# Reactor setup
# -------------------------
if __name__ == '__main__':
    factories = [
        (9009, Factory.forProtocol(C9Protocol)),
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] Twisted CTF challenges running. Connect with `nc 127.0.0.1 <port>`")
    reactor.run()
