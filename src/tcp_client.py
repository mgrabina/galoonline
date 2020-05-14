#!/usr/bin/python

import socket

server_ip = '127.0.0.1'
server_port = 9997
response_buffer_size = 4096;  # Recommended size
hostname, sld, tld, port = 'www', 'tecnico', 'ulisboa.pt', 80
target = '{}.{}.{}'.format(hostname, sld, tld)


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    return client


def send_msg(client, msg):
    msg_to_send = msg.encode()
    try:
        client.send(msg_to_send)
    except:
        print("Connection problem with " + client + ". Could not send message: " + msg)


def recv_response(client):
    try:
        return client.recv(4096).decode()
    except:
        print("Connection problem with " + client + ". Could not recieve message.")