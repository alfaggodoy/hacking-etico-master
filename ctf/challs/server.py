from twisted.internet.protocol import Factory
from twisted.internet import reactor
from retos.c1 import C1Protocol
from retos.c2 import C2Protocol
from retos.c3 import C3Protocol
from retos.c4 import C4Protocol
from retos.c5 import C5Protocol
from retos.c6 import C6Protocol
from retos.c7 import C7Protocol
from retos.c8 import C8Protocol
from retos.c9 import C9Protocol
from retos.c10 import C10Protocol

# -------------------------
# Unified CTF Server — All 10 challenges
# -------------------------
if __name__ == '__main__':
    factories = [
        (9001, Factory.forProtocol(C1Protocol)),   # C1  - Base64 Maze
        (9002, Factory.forProtocol(C2Protocol)),   # C2  - XOR Cipher
        (9003, Factory.forProtocol(C3Protocol)),   # C3  - Weak Hash Auth
        (9004, Factory.forProtocol(C4Protocol)),   # C4  - Sandboxed REPL (jailbreak)
        (9005, Factory.forProtocol(C5Protocol)),   # C5  - Simulated CMD Injection
        (9006, Factory.forProtocol(C6Protocol)),   # C6  - Caesar Shift
        (9007, Factory.forProtocol(C7Protocol)),   # C7  - Big Integer Sum
        (9008, Factory.forProtocol(C8Protocol)),   # C8  - Guess the Number
        (9009, Factory.forProtocol(C9Protocol)),   # C9  - JSON Access
        (9010, Factory.forProtocol(C10Protocol)),  # C10 - Endianness Puzzle
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] All 10 CTF challenges running!")
    print("[*] Connect with: nc 127.0.0.1 <port>")
    reactor.run()
