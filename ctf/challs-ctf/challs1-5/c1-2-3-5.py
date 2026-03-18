from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from challs.c1 import C1Protocol
from challs.c2 import C2Protocol
from challs.c3 import C3Protocol
from challs.c5 import C5Protocol

# -------------------------
# Reactor setup
# -------------------------
if __name__ == '__main__':
    factories = [
        (9001, Factory.forProtocol(C1Protocol)),
        (9002, Factory.forProtocol(C2Protocol)),
        (9003, Factory.forProtocol(C3Protocol)),
        (9005, Factory.forProtocol(C5Protocol)),
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] Twisted CTF challenges running. Connect with `nc 127.0.0.1 <port>`")
    reactor.run()
