#!/usr/bin/python

import socket, sys
import threading

bind_ip = '127.0.0.1'
bind_port = 9993
msg_buffer = 1024


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)  # max backlog of connections
    print('Listening on {}:{}'.format(bind_ip, bind_port))
    return server


def connect(server):
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    return client_sock


def start_handler(handler, client_sock):
    client_handler = threading.Thread(
        target=handler,
        args=(client_sock,)
        # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()


def recv_msg(connection):
    return connection.recv(msg_buffer).decode()


def send_msg(connection, msg):
    connection.send(msg.encode())


def close_connection(connection):
    connection.close()
