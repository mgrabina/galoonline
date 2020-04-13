#!/usr/bin/python

import socket

server_ip = '127.0.0.1'
server_port = 9993
response_buffer_size = 4096;  # Recommended size
hostname, sld, tld, port = 'www', 'tecnico', 'ulisboa.pt', 80
target = '{}.{}.{}'.format(hostname, sld, tld)


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    print('target', target)
    return client


def send_msg(client, msg):
    msg_to_send = msg.encode()
    client.send(msg_to_send)


def recv_response(client):
    return client.recv(4096).decode()
