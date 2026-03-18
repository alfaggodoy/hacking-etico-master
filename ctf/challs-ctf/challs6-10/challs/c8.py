from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import random

# -------------------------
# Challenge 8: Guess the Number
# -------------------------
class C8Protocol(Protocol):
    FLAG = "CTF_TWH3{num_gu355}"

    def connectionMade(self):
        self.secret = random.randint(0,500)
        self.transport.write(b"Welcome to Guess the Number (0-500)!\n")
        self.transport.write(b"Send guesses, I will reply 'higher' or 'lower'.\n")

    def dataReceived(self,data):

        peer = self.transport.getPeer()
        client_ip = peer.host
        client_port = peer.port
        print(f"[+] Datos recibidos de {client_ip}:{client_port} -> {data.decode()}", flush=True)

        try:
            g = int(data.strip())

        except:
            self.transport.write(b"Please send an integer.\n")
            return
        if g==self.secret:
            self.transport.write(b"Correct! Flag: "+self.FLAG.encode()+b"\n")
            self.transport.loseConnection()
        elif g<self.secret:
            self.transport.write(b"Higher!\n")
        else:
            self.transport.write(b"Lower!\n")

# -------------------------
# Reactor setup
# -------------------------
if __name__ == '__main__':
    factories = [
        (9008, Factory.forProtocol(C8Protocol)),
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] Twisted CTF challenges running. Connect with `nc 127.0.0.1 <port>`")
    reactor.run()
