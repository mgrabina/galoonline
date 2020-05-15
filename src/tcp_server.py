#!/usr/bin/python

import socket, sys
import threading

bind_ip = '127.0.0.1'
bind_port = 9991
msg_buffer = 1024


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)  # max backlog of connections
    print('Listening on {}:{}'.format(bind_ip, bind_port))
    return server


def connect(server):
    try:
        client_sock, address = server.accept()
        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        return client_sock
    except:
        print("Could not accept connection.")

def start_handler(handler, client_sock):
    try:
        client_handler = threading.Thread(
            target=handler,
            args=(client_sock,)
            # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        )
        client_handler.start()
    except:
        print("Could not handle sock.")

def recv_msg(connection):
    try:
        return connection.recv(msg_buffer).decode()
    except:
        print("Connection problem with " + connection + ". Could not recieve message.")


def send_msg(connection, msg):
    try:
        connection.send(msg.encode())
    except:
        print("Connection problem with " + connection + ". Could not send message: " + msg)


def close_connection(connection):
    try:
        connection.close()
    except:
        print("Could not close connection " + connection)