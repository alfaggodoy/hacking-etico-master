from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import binascii

# -------------------------
# Challenge 2: XOR Cipher
# -------------------------
class C2Protocol(Protocol):
    FLAG = "CTF_TWH3{x0r_4nd_b1ts}"
    KEY = 0x2A  # single-byte key used to produce the ciphertext

    def connectionMade(self):
        cipher = bytes([b ^ self.KEY for b in self.FLAG.encode()])
        msg = (
            f"""Welcome to XOR Cipher!

            The secret message has been XOR'd with a VERY simple key.

            Ciphertext (hex):
            {cipher.hex()}

            Send the key as a two-digit hex (e.g. 0f) to decode.\n"""
        )
        self.transport.write(msg.encode())

    def dataReceived(self, data):
        attempt = data.strip().decode(errors="ignore")

        peer = self.transport.getPeer()
        client_ip = peer.host
        client_port = peer.port
        print(f"[+] Datos recibidos de {client_ip}:{client_port} -> {attempt}", flush=True)

        try:
            key = int(attempt, 16)
        except Exception:
            self.transport.write(b"Please send a valid hex key (like: 0f)\n")
            return
        # decode using provided key
        cipher_hex = self.transport.session.get('c2_cipher') if hasattr(self.transport, 'session') else None
        # we recompute here for simplicity
        cipher = bytes([b ^ self.KEY for b in self.FLAG.encode()])
        decoded = bytes([b ^ key for b in cipher])
        try:
            decoded_text = decoded.decode()
        except Exception:
            decoded_text = binascii.hexlify(decoded).decode()
        if decoded_text == self.FLAG:
            self.transport.write(b"Nice! You found the key. Flag: ")
            self.transport.write(self.FLAG.encode() + b"\n")
            self.transport.loseConnection()
        else:
            self.transport.write(b"That key doesn't reveal the flag. Try another.\n")

# -------------------------
# Reactor setup
# -------------------------
if __name__ == '__main__':
    factories = [
        (9002, Factory.forProtocol(C2Protocol)),
    ]

    for port, fact in factories:
        reactor.listenTCP(port, fact)
        print(f"[*] Listening on 0.0.0.0:{port}")

    print("[*] Twisted CTF challenges running. Connect with `nc 127.0.0.1 <port>`")
    reactor.run()
