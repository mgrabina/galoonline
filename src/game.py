#!/usr/bin/python

from src import tcp_server
import queue
import itertools

connections = {}
players_statuses = {}
requests = {}
responses_queues = {}
command_separator = ' '
error_msg_prefix = "Oops! "
board = {'1': ' ', '2': ' ', '3': ' ', '4': ' ', '5': ' ', '6': ' ', '7': ' ', '8': ' ', '9': ' '}
positions = {}
symbols = {}



def push(client, msg):
    client_queue = responses_queues[connections[client]]
    if not client_queue.empty():
        tcp_server.send_msg(client, client_queue.get())
    else:
        tcp_server.send_msg(client, "UP TO DATE")


def validate_registration(client, msg):
    return client not in connections.keys() and "I".lower() not in msg[0].lower()


def validate_command(msg):
    return msg[0].lower() not in valid_commands


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
    msg_to_client = "HELLO " + username + "\n"
    connections[client] = username
    responses_queues[username] = queue.Queue()
    players_statuses[username] = "READY"
    tcp_server.send_msg(client, msg_to_client)


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
    responses_queues[requester].put("Game against " + connections[client] + " is about to start! \n")
    start_game(client, requester)


def decline_game(client, msg):
    requester = msg[1]
    if players_statuses[requester] == "READY":
        opponent_connection = find_connection(requester)
        responses_queues[requester].put(connections[client] + " didn’t accept the request or is busy")


def start_game(client, requester):
    # not yet implemented
    # aux = [requester, connections[client]]
    # starter = random.choice(aux)
    symbols[requester] = 'X'
    symbols[connections[client]] = 'O'
    tcp_server.send_msg(client, "\n" + connections[client] + "'s turn \n")
    tcp_server.send_msg(find_connection(requester), "\n" + connections[client] + "'s turn \n")


def turns(client):
    players = symbols.keys()
    for player in players:
        if player == connections[client]:
            tcp_server.send_msg(client, "\n" + connections[player] + "'s turn \n")
        else:
            responses_queues[player].put("\n" + connections[player] + "'s turn \n")
           # tcp_server.send_msg(find_connection(player), "\n" + connections[client] + "'s turn \n")



def show_board():
    players = symbols.keys()
    for player in players:
        tcp_server.send_msg(find_connection(player), board_str())


def board_str():
    str = ""
    str += ("\n" + board['1'] + '|' + board['2'] + '|' + board['3'] + "\n"
            + "-----\n"
            + board['4'] + '|' + board['5'] + '|' + board['6'] + "\n"
            + '-----\n' +
            board['7'] + '|' + board['8'] + '|' + board['9'] + "\n")
    return str


def new_move(client, msg):
    row = msg[1]
    col = msg[2]
    played = 0

    if row == "1":
        if col == "1":
            if board['1'] == ' ':
                positions[connections[client]] = 1
                board['1'] = symbols[connections[client]]
                played = 1

        if col == "2":
            if board['2'] == ' ':
                positions[connections[client]] = 2
                board['2'] = symbols[connections[client]]
                played = 1

        if col == "3":
            if board['3'] == ' ':
                positions[connections[client]] = 3
                board['3'] = symbols[connections[client]]
                played = 1
    if row == "2":
        if col == "1":
            if board['4'] == ' ':
                positions[connections[client]] = 4
                board['4'] = symbols[connections[client]]
                played = 1

        if col == "2":
            if board['5'] == ' ':
                positions[connections[client]] = 5
                board['5'] = symbols[connections[client]]
                played = 1

        if col == "3":
            if board['6'] == ' ':
                positions[connections[client]] = 6
                board['6'] = symbols[connections[client]]
                played = 1
    if row == "3":
        if col == "1":
            if board['7'] == ' ':
                positions[connections[client]] = 7
                board['7'] = symbols[connections[client]]
                played = 1

        if col == "2":
            if board['8'] == ' ':
                positions[connections[client]] = 8
                board['8'] = symbols[connections[client]]
                played = 1

        if col == "3":
            if board['9'] == ' ':
                positions[connections[client]] = 9
                board['9'] = symbols[connections[client]]
                played = 1
    if played == 0:
        tcp_server.send_msg(client, "Invalid play \n")
    show_board()
    turns(client)



def clean_board():
    for key in board:
        board[key] = ' '


def clean_positions():
    for key in positions:
        positions[key] = ' '


def clean_symbols():
    for key in symbols:
        symbols[key] = ' '


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
