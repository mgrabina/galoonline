#!/usr/bin/python

from src import tcp_server
from src import game


def client_handler(client):
    while True:
        msg = tcp_server.recv_msg(client).split(game.command_separator)
        # Validate Command
        if game.validate_command(msg):
            tcp_server.send_msg(client, game.error_msg_prefix + "Invalid command")
            continue
        # Validate Registry
        if game.validate_registration(client, msg):
            tcp_server.send_msg(client, game.error_msg_prefix + "Please register first.")
            continue
        # Then execute game action
        game.commands_handler.get(msg[0].lower())(client, msg)


server = tcp_server.start_server()
while True:
    connection = tcp_server.connect(server)
    tcp_server.start_handler(client_handler, connection)
