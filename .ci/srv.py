import os
import socket

from numpy.random import default_rng


def server_program(seed=0):
    # get the hostname
    host = os.getenv("ATF_SOCKET_HOST", "localhost")
    port = os.getenv("ATF_SOCKET_PORT", 5000)  # initiate port no above 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    data = "greeting"
    conn.send(data.encode())  # send data to the client

    rng = default_rng(seed)

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        data = str(data)
        print(f"from connected user: {data}")
        if data.startswith("GETCHIDX"):
            reply = f"{rng.integers(0, 100)}"
            print(f"reply to client: {reply}")
            conn.send(reply.encode())  # send data to the client
        elif data.startswith(("GETRS", "GETDS")):
            reply = f"{rng.random()}"
            print(f"reply to client: {reply}")
            conn.send(reply.encode())  # send data to the client
        else:
            print(f"{data = }")
    conn.close()  # close the connection


if __name__ == "__main__":
    server_program()