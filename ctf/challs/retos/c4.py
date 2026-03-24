from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import os

# -------------------------
# Challenge 4: Sandboxed REPL (jailbreak)
# -------------------------
class C4Protocol(Protocol):
    FLAG_FILENAME = 'flag4.txt'
    FLAG = "CTF_TWH3{r3pl_3sc4p3}"

    def connectionMade(self):
        # Escribe la flag en un fichero que el sandbox escape intentará leer
        with open(self.FLAG_FILENAME, 'w') as f:
            f.write(self.FLAG + "\n")

        msg = (
            "Welcome to the 'restricted' Python REPL.\n"
            "Only expressions are evaluated with a minimal environment.\n"
            "Try to get the content of the file 'flag4.txt'.\n"
            "Send an expression followed by newline. Type 'quit' to exit.\n"
        )
        self.transport.write(msg.encode())

    def dataReceived(self, data):
        expr = data.strip().decode(errors="ignore")

        peer = self.transport.getPeer()
        client_ip = peer.host
        client_port = peer.port
        print(f"[+] Datos recibidos de {client_ip}:{client_port} -> {expr}")

        if expr.lower() == 'quit':
            self.transport.write(b"Bye!\n")
            self.transport.loseConnection()
            return

        # Entorno intencionalmente inseguro (CTF learning)
        # builtins=None pero sigue siendo vulnerable a introspección de objetos
        try:
            result = eval(expr, {'__builtins__': None}, {})
            self.transport.write(repr(result).encode() + b"\n")
        except Exception as e:
            self.transport.write(f"Error: {e}\n".encode())

# -------------------------
# Reactor setup (standalone)
# -------------------------
if __name__ == '__main__':
    factories = [
        (9004, Factory.forProtocol(C4Protocol)),
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] Twisted CTF challenges running. Connect with `nc 127.0.0.1 <port>`")
    reactor.run()
