#!/usr/bin/python

from src import tcp_server
import queue

connections = {}
players_statuses = {}
requests = {}
responses_queues = {}
command_separator = ' '
error_msg_prefix = "Oops! "


def push(client, msg):
    client_queue = responses_queues[connections[client]]
    if not client_queue.empty():
        tcp_server.send_msg(client, client_queue.get())
    else:
        tcp_server.send_msg(client, "UP TO DATE")


def validate_registration(client, msg):
    return client not in connections.keys() and "I".lower() not in msg[0].lower()


def validate_command(msg):
    return msg[0] not in valid_commands


def find_connection(username):
    for key in connections:
        if connections[key] == username:
            return key
    return None


def parse_dic(dic):
    str = ""
    for key in dic:
        str += (key + ": " + dic[key] + "\n")
    return str


def register_new_player(client, msg):
    # TODO: Validate msg format
    username = msg[2]
    msg_to_client = 'HELLO ' + username
    connections[client] = username
    responses_queues[username] = queue.Queue()
    players_statuses[username] = "READY"
    tcp_server.send_msg(client, msg_to_client)
    print(client)


def check_status(client, msg):
    # TODO: Develop function
    print("")


def get_players_list(client, msg):
    # TODO: Develop function
    tcp_server.send_msg(client, parse_dic(players_statuses))  # TODO: Format text


def request_new_game(client, msg):
    opponent = msg[1]
    if players_statuses[opponent] != "READY":
        tcp_server.send_msg(client, opponent + " didn’t accept the request or is busy.")
    opponent_connection = find_connection(opponent)
    if opponent_connection is None:
        tcp_server.send_msg(client, opponent + " didn’t accept the request or is busy.")
    requests[connections[client]] = opponent
    tcp_server.send_msg(client, "waiting " + opponent + " response…")
    responses_queues[opponent].put(connections[client] + " wants to play!")


def accept_game(client, msg):
    requester = msg[1]
    if players_statuses[requester] != "READY":
        tcp_server.send_msg(client, requester + " didn’t accept the request or is busy.")
    opponent_connection = find_connection(requester)
    if opponent_connection is None:
        tcp_server.send_msg(client, requester + " didn’t accept the request or is busy.")
    players_statuses[connections[client]] = "BUSY"
    players_statuses[requester] = "BUSY"
    tcp_server.send_msg(client, "Game against " + requester + " is about to start!")
    responses_queues[requester].put("Game against " + connections[client] + " is about to start!")


def decline_game(client, msg):
    requester = msg[1]
    if players_statuses[requester] == "READY":
        opponent_connection = find_connection(requester)
        responses_queues[requester].put(connections[client] + " didn’t accept the request or is busy")


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
    'exit': logout,
    'push': push
}
valid_commands = commands_handler.keys()
