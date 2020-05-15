#!/usr/bin/python
import os
import socket

server_ip = '127.0.0.1'
server_port = 9994
response_buffer_size = 4096;  # Recommended size
hostname, sld, tld, port = 'www', 'tecnico', 'ulisboa.pt', 80
target = '{}.{}.{}'.format(hostname, sld, tld)


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    return client


def close_conn(server: socket.socket):
    print("Closing connection with server. Ending session. Goodbye.")
    server.shutdown(socket.SHUT_WR)
    server.close()
    os._exit(0)


def send_msg(client: socket.socket, msg):
    msg_to_send = msg.encode()
    try:
        client.send(msg_to_send)
    except:
        print("Connection problem with " + client + ". Could not send message")
        close_conn(client)


def recv_response(client):
    try:
        recv = client.recv(4096).decode()
        if len(recv) > 0:
            return recv
        close_conn(client)
    except:
        print("Connection problem with " + client + ". Could not recieve message.")
        close_conn(client)