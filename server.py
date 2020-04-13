#!/usr/bin/python

from src import tcp_server

connections = {}
players_statuses = {}
command_separator = ' '
error_msg_prefix = "Oops! "


def register_new_player(client, msg):
    # TODO: Validate msg format
    username = msg[2]
    msg_to_client = 'HELLO ' + username
    connections[client] = username
    players_statuses[username] = "READY"
    tcp_server.send_msg(client, msg_to_client)
    print(client)


def check_status(client, msg):
    # TODO: Develop function
    print("")


def get_players_list(client, msg):
    # TODO: Develop function
    tcp_server.send_msg(client, str(players_statuses))  # TODO: Format text


def request_new_game(client, msg):
    # TODO: Develop function
    print("")


def accept_game(client, msg):
    # TODO: Develop function
    print("")


def decline_game(client, msg):
    # TODO: Develop function
    print("")


def new_move(client, msg):
    # TODO: Develop function
    print("")


def logout(client, msg):
    tcp_server.send_msg(client, "Bye " + connections[client])
    tcp_server.close_connection(client)
    # TODO: Develop function
    print("")


commands_handler = {
    'i': register_new_player,
    'ok?': check_status,
    'players': get_players_list,
    'play': request_new_game,
    'accept': accept_game,
    'decline': decline_game,
    'move': new_move,
    'exit': logout
}
valid_commands = commands_handler.keys()


def client_handler(client):
    while True:
        msg = tcp_server.recv_msg(client).split(command_separator)
        # Validate Command
        if msg[0] not in valid_commands:
            tcp_server.send_msg(client, error_msg_prefix + "Invalid command")
            continue
        # Validate Registry
        if client not in connections.keys() and "I".lower() not in msg[0].lower():
            tcp_server.send_msg(client, error_msg_prefix + "Please register first.")
            continue
        commands_handler.get(msg[0].lower())(client, msg)


server = tcp_server.start_server()
while True:
    connection = tcp_server.connect(server)
    tcp_server.start_handler(client_handler, connection)
