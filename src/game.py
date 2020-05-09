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
active = {}
plays = 0


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


def check_status(client):
    tcp_server.send_msg(client, "ok" + connections[client]+"\n")



def get_players_list(client):
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
    # responses_queues[opponent].put(connections[client] + " wants to play!")
    tcp_server.send_msg(find_connection(opponent), connections[client] + " wants to play!")


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
    tcp_server.send_msg(find_connection(requester), "Game against " + connections[client] + " is about to start!")
    # responses_queues[requester].put("Game against " + connections[client] + " is about to start! \n")
    start_game(client, requester)


def decline_game(client, msg):
    requester = msg[1]
    if players_statuses[requester] == "READY":
        opponent_connection = find_connection(requester)
        # responses_queues[requester].put(connections[client] + " didn’t accept the request or is busy")
        tcp_server.send_msg(find_connection(requester), connections[client] + " didn’t accept the request or is busy")


def start_game(client, requester):
    symbols[requester] = 'X'
    symbols[connections[client]] = 'O'
    tcp_server.send_msg(client, "\nYour turn \n")
    tcp_server.send_msg(find_connection(requester), "\n" + connections[client] + "'s turn \n")
    show_board()
    active[connections[client]] = "true"
    active[requester] = "false"


def turns(client):
    players = symbols.keys()
    for player in players:
        if player != connections[client]:
            tcp_server.send_msg(client, "\n" + player + "'s turn \n")
            tcp_server.send_msg(find_connection(player), "\nYour turn \n")


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
    global plays
    if symbols:
        if row == "1":
            if col == "1":
                if board['1'] == ' ':
                    positions[connections[client]] = 1
                    board['1'] = symbols[connections[client]]
                    played = 1

            elif col == "2":
                if board['2'] == ' ':
                    positions[connections[client]] = 2
                    board['2'] = symbols[connections[client]]
                    played = 1

            elif col == "3":
                if board['3'] == ' ':
                    positions[connections[client]] = 3
                    board['3'] = symbols[connections[client]]
                    played = 1
        elif row == "2":
            if col == "1":
                if board['4'] == ' ':
                    positions[connections[client]] = 4
                    board['4'] = symbols[connections[client]]
                    played = 1

            elif col == "2":
                if board['5'] == ' ':
                    positions[connections[client]] = 5
                    board['5'] = symbols[connections[client]]
                    played = 1

            elif col == "3":
                if board['6'] == ' ':
                    positions[connections[client]] = 6
                    board['6'] = symbols[connections[client]]
                    played = 1
        elif row == "3":
            if col == "1":
                if board['7'] == ' ':
                    positions[connections[client]] = 7
                    board['7'] = symbols[connections[client]]
                    played = 1

            elif col == "2":
                if board['8'] == ' ':
                    positions[connections[client]] = 8
                    board['8'] = symbols[connections[client]]
                    played = 1

            elif col == "3":
                if board['9'] == ' ':
                    positions[connections[client]] = 9
                    board['9'] = symbols[connections[client]]
                    played = 1
        if played == 0:
            tcp_server.send_msg(client, "Invalid play \n")
        else:
            plays = plays + 1
            show_board()
            turns(client)
            if 5 <= plays < 9:
                verify_winner(client)
            if plays == 9:
                tcp_server.send_msg(client, "It's a tie \n")
                reset_game()

    else:
        tcp_server.send_msg(client, "Not enrolled in a game \n")


def winner_msg(symbol):
    winner = ''
    for key in symbols:
        if symbols[key] == symbol:
            winner = key
        tcp_server.send_msg(find_connection(key), "Game over!" + winner + "wins")
        players_statuses[key] = "READY"

    reset_game()


def verify_winner(client):
    if board['1'] == board['2'] == board['3'] and board['1'] != ' ':
        winner_msg(board['1'])
    elif board['1'] == board['4'] == board['7'] and board['1'] != ' ':
        winner_msg(board['1'])
    elif board['1'] == board['5'] == board['9'] and board['1'] != ' ':
        winner_msg(board['1'])
    elif board['2'] == board['5'] == board['8'] and board['2'] != ' ':
        winner_msg(board['2'])
    elif board['3'] == board['6'] == board['9'] and board['3'] != ' ':
        winner_msg(board['3'])
    elif board['4'] == board['5'] == board['6'] and board['4'] != ' ':
        winner_msg(board['4'])
    elif board['7'] == board['8'] == board['9'] and board['7'] != ' ':
        winner_msg(board['7'])
    elif board['7'] == board['5'] == board['3'] and board['7'] != ' ':
        winner_msg(board['7'])



def reset_game():
    clean_board()
    positions.clear()
    symbols.clear()
    active.clear()


def clean_board():
    for key in board.keys():
        board[key] = ' '


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
