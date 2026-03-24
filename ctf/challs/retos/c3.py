from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import hashlib

# -------------------------
# Challenge 3: Weak Hash Compare
# -------------------------
class C3Protocol(Protocol):
    SALT = "s0m3_s4lt"
    SECRET_PASSWORD = "letmein123"
    FLAG = "CTF_TWH3{h45h_trunc_weak}"

    # server stores truncated hash (first 6 hex chars)
    TOKEN_FULL = hashlib.sha256((SALT + SECRET_PASSWORD).encode()).hexdigest()
    TOKEN_TRUNC = TOKEN_FULL[:6]

    def connectionMade(self):
        # leak the truncated token to make the challenge solvable by offline collision search
        msg = (
            f"""Welcome to Weak Hash Auth!

            Authenticate as 'admin' by sending its password.

            NOTE: the server only compares the FIRST 6 hex digits of the sha256(salt+password).

            Stored truncated token (first 6 hex chars): {self.TOKEN_TRUNC}

            Send password followed by newline.
            
            DO NOT BRUTEFORCE THIS VIA SOCKET, DO IT OFFLINE, YOU MIGHT GET IP-BANNED FROM THE CTF.\n"""
        )
        self.transport.write(msg.encode())

    def dataReceived(self, data):
        hint = """
-------------[HINT]-------------
SALT = "s0m3_s4lt"
SECRET_PASSWORD = b"BRUTE_ME"
data = SECRET_PASSWORD
attempt = data.strip().decode(errors="ignore")
digest = hashlib.sha256((self.SALT + attempt).encode()).hexdigest()
if digest[:6] == self.TOKEN_TRUNC:
    self.transport.write(b"Authenticated! Here is your flag: ")
    self.transport.write(self.FLAG.encode() + b"\\n")
    self.transport.loseConnection()
else:
    self.transport.write(b"Authentication failed.\\n")
-------------[HINT]-------------\n
"""
        attempt = data.strip().decode(errors="ignore")

        peer = self.transport.getPeer()
        client_ip = peer.host
        client_port = peer.port
        print(f"[+] Datos recibidos de {client_ip}:{client_port} -> {attempt}", flush=True)

        digest = hashlib.sha256((self.SALT + attempt).encode()).hexdigest()
        if digest[:6] == self.TOKEN_TRUNC:
            self.transport.write(b"Authenticated! Here is your flag: ")
            self.transport.write(self.FLAG.encode() + b"\n")
            self.transport.loseConnection()
        else:
            self.transport.write(b"Authentication failed.\n")
            self.transport.write(hint.encode() + b"\n")


# -------------------------
# Reactor setup
# -------------------------
if __name__ == '__main__':
    factories = [
        (9003, Factory.forProtocol(C3Protocol)),
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] Twisted CTF challenges running. Connect with `nc 127.0.0.1 <port>`")
    reactor.run()
