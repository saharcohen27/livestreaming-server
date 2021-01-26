import socket
import random
import os
from streamProtocol import RTMP
from DataBase import Database
from streamer import Streamer

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = '127.0.0.1' # = localhost
port = 1935
server_address = (addr, port)
BUFFER = RTMP.BUFFER

# Bind the socket to the port
try:
    sock.bind(server_address)
except OSError:
    print("[ERROR] Server is already running on this port.")
    exit()

# Listen for incoming connections
max_connections = 1024
sock.listen(max_connections)

print(f"Server running on {addr}:{port}. Maximum Connections: {max_connections}.")

conn, client_address = sock.accept()
streamer = Streamer(conn)

# Logic
while conn.fileno() != -1:
    data = conn.recv(BUFFER)
    
    # print("Data | >>> ", ''.join(r'\x'+hex(letter)[2:] for letter in data[0:40]))
    
    if not data:
        streamer.stop_live()
        print("User disconnected!")
        break


    if data[0] == 3 and len(data) == 1537:
        # the handshake starts from client side. '3' + 1536 random bytes 
        RTMP().handshake(conn, data)
    
    if b"connect" in data:
        # after user ask to connect we need to set the chunk size and send him result message
        RTMP().set_chunk_size(conn)
        conn.send(RTMP()._result())
    
    if b"releaseStream" in data:
        key_index = data.index(b"releaseStream") + 26
        stream_key = str(data[key_index:key_index + 36])[2:-1] # to remove the b''
        if Database().valid_stream_key(stream_key):
            streamer.set_stream_key(stream_key)
        else:
            conn.close()
            break

    if b"Publish" in data:
        streamer.start_live()

    if b"createStream" in data:
        conn.send(RTMP().OnStatus())

    if b"onMetaData" in data:
        streamer.set_stream_settings(RTMP().onMetaData(data))

    if streamer.live_on():
        streamer.handle_stream(data)


