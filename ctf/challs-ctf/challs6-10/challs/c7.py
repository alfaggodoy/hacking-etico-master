from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import random

# -------------------------
# Challenge 7: Big Integer Sum
# -------------------------
class C7Protocol(Protocol):
    FLAG = "CTF_TWH3{b1g_num5_sum}"

    def connectionMade(self):
        a = random.getrandbits(200)
        b = random.getrandbits(200)
        self.secret_sum = a+b
        self.transport.write(b"Welcome to Big Integer Sum!\n")
        self.transport.write(f"Add these numbers exactly and send result:\n{a}\n{b}\n".encode())

    def dataReceived(self,data):
        attempt = data.strip().decode(errors="ignore")

        peer = self.transport.getPeer()
        client_ip = peer.host
        client_port = peer.port
        print(f"[+] Datos recibidos de {client_ip}:{client_port} -> {attempt}", flush=True)
        
        try:
            if int(attempt)==self.secret_sum:
                self.transport.write(b"Correct! Flag: "+self.FLAG.encode()+b"\n")
                self.transport.loseConnection()
                return
        except:
            pass
        self.transport.write(b"Incorrect.\n")

# -------------------------
# Reactor setup
# -------------------------
if __name__ == '__main__':
    factories = [
        (9007, Factory.forProtocol(C7Protocol)),
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] Twisted CTF challenges running. Connect with `nc 127.0.0.1 <port>`")
    reactor.run()
