import socket
import re
from typing import Union


class NetworkSocket:
    def __init__(self, host="localhost", port=13050, timeout=5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.connected = False
        self.socket = None
        self.buffer = b""

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.connect((self.host, self.port))
        self.connected = True

    def close(self):
        self.socket.close()
        self.connected = False

    def send(self, data: bytes):
        self.socket.sendall(data)

    def receive(self) -> Union[bytes, None]:
        regex = re.compile(br"<(room[\s\S]+?</room>|.*?/>)")
        while True:
            try:
                chunk = self.socket.recv(16129)
            except socket.timeout:
                chunk = b""
            except ConnectionResetError:
                self.close()
                return None
            if chunk:
                self.buffer += chunk
                if regex.search(self.buffer):
                    receive = regex.search(self.buffer).group()
                    self.buffer = self.buffer.replace(receive, b"")
                    return receive
            else:
                return None
