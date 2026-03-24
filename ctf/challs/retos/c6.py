from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import random

# -------------------------
# Challenge 6: Caesar Shift
# -------------------------
class C6Protocol(Protocol):
    FLAG = "CTF_TWH3{c43s4r_sh1ft}"

    def connectionMade(self):
        shift = random.randint(1,25)
        cipher = ''.join(chr(((ord(c)-65+shift)%26)+65) if c.isupper() else chr(((ord(c)-97+shift)%26)+97) if c.islower() else c for c in self.FLAG)
        self.transport.write(b"Welcome!\n")
        self.transport.write(f"Ciphertext: {cipher}\n".encode())
        self.transport.write(b"Send the decoded flag.\n")

    def dataReceived(self,data):
        attempt = data.strip().decode(errors="ignore")

        peer = self.transport.getPeer()
        client_ip = peer.host
        client_port = peer.port
        print(f"[+] Datos recibidos de {client_ip}:{client_port} -> {attempt}", flush=True)

        if attempt == self.FLAG:
            self.transport.write(b"Correct! Flag: "+self.FLAG.encode()+b"\n")
            self.transport.loseConnection()
        else:
            self.transport.write(b"Nope.\n")

# -------------------------
# Reactor setup
# -------------------------
if __name__ == '__main__':
    factories = [
        (9006, Factory.forProtocol(C6Protocol)),
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] Twisted CTF challenges running. Connect with `nc 127.0.0.1 <port>`")
    reactor.run()
