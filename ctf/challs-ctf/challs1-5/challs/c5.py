from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

# -------------------------
# Challenge 5: Simulated Command Injection
# -------------------------
class C5Protocol(Protocol):
    FLAG = "CTF_TWH3{s1mul4t3d_cmd_inj}"
    FILES = ['notes.txt', 'todo.txt', 'readme.md', 'backup.log', 'flag.txt']

    def connectionMade(self):
        msg = (
            "Welcome to TinySearch!\n"
            "Usage: send 'search <pattern>' and we will show matching filenames.\n"
        )
        self.transport.write(msg.encode())

    def dataReceived(self, data):
        line = data.strip().decode(errors="ignore")

        peer = self.transport.getPeer()
        client_ip = peer.host
        client_port = peer.port
        print(f"[+] Datos recibidos de {client_ip}:{client_port} -> {line}", flush=True)

        if line.startswith('help'):
            self.transport.write(b"""Commands:
                                 search <pattern> (ALL USERS)
                                 reveal (ADMIN ONLY)\n""")
            return
        if not line.startswith('search '):
            self.transport.write(b"Invalid command. Try: help\n")
            return
        payload = line[len('search '):]
        # naive parsing that splits on semicolon
        parts = payload.split(';')
        pattern = parts[0].strip()
        matches = [fn for fn in self.FILES if pattern in fn]
        if len(parts) > 1:
            admin = parts[1].strip()
            if admin == 'reveal':
                self.transport.write(b"ADMIN: revealing secret...\n")
                self.transport.write(self.FLAG.encode() + b"\n")
                self.transport.loseConnection()
                return
            else:
                self.transport.write(b"ADMIN: unknown command\n")
                return
        if matches:
            self.transport.write(b"Matches:\n")
            for m in matches:
                self.transport.write(m.encode() + b"\n")
        else:
            self.transport.write(b"No matches found.\n")

# -------------------------
# Reactor setup
# -------------------------
if __name__ == '__main__':
    factories = [
        (9005, Factory.forProtocol(C5Protocol)),
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] Twisted CTF challenges running. Connect with `nc 127.0.0.1 <port>`")
    reactor.run()
