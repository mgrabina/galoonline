#!/usr/bin/python
import threading
import socket
from concurrent.futures.thread import ThreadPoolExecutor

from src import tcp_server
from src import logic


def client_handler(client: socket.socket):
    logic.menu(client)
    while True:

        msg = tcp_server.recv_msg(client)
        if msg is not None:
            msg = msg.split()

        # Validate Command
        if logic.validate_command(msg):
            tcp_server.send_msg(client, logic.error_msg_prefix + "Invalid command")
            continue
        # Validate Registry
        if logic.validate_registration(client, msg) and 'exit' not in msg:
            tcp_server.send_msg(client, logic.error_msg_prefix + "Please register first. \n")
            continue
        # Then execute game action

        try:
            threading.Thread(target=logic.commands_handler.get(msg[0].lower()), args=(client, msg,)).start()
        except:
            if client.fileno() == -1:
                break
            tcp_server.send_msg(client, "There was a problem procesing your request\n")


server = tcp_server.start_server()
while True:
    connection = tcp_server.connect(server)
    tcp_server.start_handler(client_handler, connection)
