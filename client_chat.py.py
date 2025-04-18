# server_chat.py
import socket

HOST = '0.0.0.0'  # hört auf allen Interfaces
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("Server läuft. Warte auf Verbindung...")

conn, addr = server.accept()
print(f"Verbunden mit {addr}")

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print(f"Client: {data}")
    antwort = input("Du (Server): ")
    conn.send(antwort.encode())
