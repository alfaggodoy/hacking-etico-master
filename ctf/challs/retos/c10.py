from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import random

# -------------------------
# Challenge 10: Endianness Puzzle
# -------------------------
class C10Protocol(Protocol):
    FLAG = "CTF_TWH3{3nd14nn3ss}"

    def connectionMade(self):
        val = random.randint(0,2**32-1)
        hexstr = f"{val:08x}"
        # little endian repr
        b = bytes.fromhex(hexstr)
        le = b[::-1].hex()
        self.answer = int(hexstr,16)
        self.transport.write(b"Welcome to Endianness Puzzle!\n")
        self.transport.write(f"Here is a 32-bit hex value (little-endian bytes): {le}\n".encode())
        self.transport.write(b"Send the decimal value when interpreted in big-endian.\n")

    def dataReceived(self,data):

        peer = self.transport.getPeer()
        client_ip = peer.host
        client_port = peer.port
        print(f"[+] Datos recibidos de {client_ip}:{client_port} -> {data.decode()}", flush=True)

        try:
            g = int(data.strip())

        except:
            self.transport.write(b"Send a decimal integer.\n")
            return
        if g==self.answer:
            self.transport.write(b"Correct! Flag: "+self.FLAG.encode()+b"\n")
            self.transport.loseConnection()
        else:
            self.transport.write(b"Wrong.\n")

# -------------------------
# Reactor setup
# -------------------------
if __name__ == '__main__':
    factories = [
        (9010, Factory.forProtocol(C10Protocol)),
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] Twisted CTF challenges running. Connect with `nc 127.0.0.1 <port>`")
    reactor.run()
