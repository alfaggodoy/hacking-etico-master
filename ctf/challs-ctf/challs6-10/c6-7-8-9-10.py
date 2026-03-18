from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from challs.c6 import C6Protocol
from challs.c7 import C7Protocol
from challs.c8 import C8Protocol
from challs.c9 import C9Protocol
from challs.c10 import C10Protocol

# -------------------------
# Reactor setup
# -------------------------
if __name__ == '__main__':
    factories = [
        (9006, Factory.forProtocol(C6Protocol)),
        (9007, Factory.forProtocol(C7Protocol)),
        (9008, Factory.forProtocol(C8Protocol)),
        (9009, Factory.forProtocol(C9Protocol)),
        (9010, Factory.forProtocol(C10Protocol))
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] Twisted CTF challenges running. Connect with `nc 127.0.0.1 <port>`")
    reactor.run()
