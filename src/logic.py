#!/usr/bin/python

from src import tcp_server
from src.game import Game
import itertools

connections = {}
players_statuses = {}
requests = {}
command_separator = ' '
error_msg_prefix = "Oops! "
menu_commands = "Available commands:\n" \
                "- I AM <username> : register\n" \
                "- OK? : check status\n" \
                "- Players : get players list\n" \
                "- Play <username> : request a new game\n" \
                "- Accept <username>: accept game\n" \
                "- Decline <username>: decline game\n" \
                "- Move <row> <col> : new move\n" \
                "- exit : exit game\n"
welcome_message = "\nWelcome to Galo Online!\n"
games = {}


def validate_registration(client, msg):
    if msg and len(msg) > 0:
        return client not in connections.keys() and len(msg[0]) != 1
    return False


def validate_command(msg):
    if msg and len(msg) > 0:
        return msg[0].lower() not in valid_commands
    return False

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
    if len(msg) != 3 or msg[1].lower() != 'am' or msg[2] == '':
        tcp_server.send_msg(client, "Invalid format!\n")
    elif client in connections:
        tcp_server.send_msg(client, "Already registered!\n")
    elif msg[2] in connections.values():
        tcp_server.send_msg(client, "Repeated username\n")
    else:
        username = msg[2]
        msg_to_client = "HELLO " + username + "\n"
        connections[client] = username
        players_statuses[username] = "READY"
        tcp_server.send_msg(client, msg_to_client)


def check_status(client, msg):
    tcp_server.send_msg(client, "OK " + connections[client] + "\n")


def get_players_list(client, msg):
    tcp_server.send_msg(client, parse_dic(players_statuses))


def request_new_game(client, msg):
    if len(msg) == 2:
        opponent = msg[1]
        if opponent == connections[client]:
            tcp_server.send_msg(client, "Cannot play against you!\n")
            return
        if not opponent in players_statuses:
            tcp_server.send_msg(client, opponent + " not found.\n")
            return
        if players_statuses[opponent] != "READY":
            tcp_server.send_msg(client, opponent + " didn’t accept the request or is busy.\n")
            return
        opponent_connection = find_connection(opponent)
        if opponent_connection is None:
            tcp_server.send_msg(client, opponent + " didn’t accept the request or is busy.\n")
            return
        requests[connections[client]] = opponent
        tcp_server.send_msg(client, "waiting " + opponent + " response…")
        tcp_server.send_msg(find_connection(opponent), connections[client] + " wants to play!")
    else:
        tcp_server.send_msg(client, "Please introduce a valid Play <username> request  \n")


def accept_game(client, msg):
    if len(msg) == 2:
        requester = msg[1]
        if requests[requester] != connections[client]:
            tcp_server.send_msg(client, requester + " didn’t accept the request or is busy.\n")
        if players_statuses[requester] != "READY":
            tcp_server.send_msg(client, requester + " didn’t accept the request or is busy.\n")
        opponent_connection = find_connection(requester)
        if opponent_connection is None:
            tcp_server.send_msg(client, requester + " didn’t accept the request or is busy.\n")
        players_statuses[connections[client]] = "BUSY"
        players_statuses[requester] = "BUSY"
        del requests[requester]
        tcp_server.send_msg(client, "Game against " + requester + " is about to start!\n")
        tcp_server.send_msg(find_connection(requester), "Game against " + connections[client] + " is about to start!")
        start_game(client, requester)
    else:
        tcp_server.send_msg(client, "Please introduce a valid Accept <username> request  \n")


def decline_game(client, msg):
    if len(msg) == 2:
        requester = msg[1]
        del requests[requester]
        if players_statuses[requester] == "READY":
            opponent_connection = find_connection(requester)
            tcp_server.send_msg(find_connection(requester),
                                connections[client] + " didn’t accept the request or is busy \n")
    else:
        tcp_server.send_msg(client, "Please introduce a valid Decline <username> request  \n")


def start_game(client, requester):
    requester_connection = find_connection(requester)
    new_game = Game(requester_connection, client, requester, connections[client])
    games[client] = new_game
    games[requester_connection] = new_game
    show_board(new_game)
    next_turn(new_game)


def next_turn(current_game):
    current_game.change_turn()
    if current_game.active == current_game.opponent_username:
        tcp_server.send_msg(current_game.requester_connection, "\n" + current_game.opponent_username + "'s turn \n")
        tcp_server.send_msg(current_game.opponent_connection, "\nYour turn \n")
    else:
        tcp_server.send_msg(current_game.opponent_connection, "\n" + current_game.requester_username + "'s turn \n")
        tcp_server.send_msg(current_game.requester_connection, "\nYour turn \n")


def show_board(current_game: Game):
    tcp_server.send_msg(current_game.requester_connection, board_str(current_game.board))
    tcp_server.send_msg(current_game.opponent_connection, board_str(current_game.board))


def board_str(board):
    str = ""
    str += ("\n " + board[0][0] + ' | ' + board[0][1] + ' | ' + board[0][2] + "\n"
            + "-----------\n "
            + board[1][0] + ' | ' + board[1][1] + ' | ' + board[1][2] + "\n"
            + '-----------\n ' +
            board[2][0] + ' | ' + board[2][1] + ' | ' + board[2][2] + "\n")
    return str


def new_move(client, msg):
    if len(msg) == 3:
        row = int(msg[1]) - 1
        col = int(msg[2]) - 1
        if games[client]:
            current_game = games[client]
            if current_game.active == connections[client]:
                if 0 <= row <= 2 and 0 <= col <= 2 and current_game.board[row][col] == ' ':
                    current_game.board[row][col] = current_game.symbols[current_game.active]
                    current_game.moves += 1
                    show_board(current_game)
                    if 5 <= current_game.moves <= 9:
                        winner = verify_winner(current_game)
                        if winner is not None:
                            winner_username = current_game.username_by_symbol(winner)
                            tcp_server.send_msg(current_game.requester_connection,
                                                "Game over! " + winner_username + " wins\n")
                            tcp_server.send_msg(current_game.opponent_connection,
                                                "Game over! " + winner_username + " wins\n")
                            reset_game(current_game)
                            return
                        elif current_game.moves == 9:
                            tcp_server.send_msg(current_game.requester_connection, "It's a tie \n")
                            tcp_server.send_msg(current_game.opponent_connection, "It's a tie \n")
                            reset_game(current_game)
                            return
                    next_turn(current_game)
                else:
                    tcp_server.send_msg(client, "Invalid play \n")
            else:
                tcp_server.send_msg(client, "Please wait for your turn \n")
        else:
            tcp_server.send_msg(client, "Not enrolled in a game \n")
    else:
        tcp_server.send_msg(client, "Please introduce a valid <row><column> move \n")


def verify_winner(current_game: Game):
    winner = None
    for i in [0, 1, 2]:
        if current_game.board[i][0] == current_game.board[i][1] == current_game.board[i][2]:
            winner = current_game.board[i][0]
            break
        if current_game.board[0][i] == current_game.board[1][i] == current_game.board[2][i]:
            winner = current_game.board[0][i]
            break
    if current_game.board[0][0] == current_game.board[1][1] == current_game.board[2][2]:
        winner = current_game.board[0][0]
    if current_game.board[0][2] == current_game.board[1][1] == current_game.board[2][0]:
        winner = current_game.board[0][2]
    return winner


def reset_game(current_game: Game):
    del games[current_game.requester_connection]
    del games[current_game.opponent_connection]
    players_statuses[current_game.requester_username] = "READY"
    players_statuses[current_game.opponent_username] = "READY"
    menu(current_game.requester_connection)
    menu(current_game.opponent_connection)


def menu(client):
    tcp_server.send_msg(client, welcome_message)
    tcp_server.send_msg(client, menu_commands)


def logout(client, msg):
    if client not in connections:
        tcp_server.send_msg(client, "Bye")
        tcp_server.close_connection(client)
        return
    if connections[client] and players_statuses[connections[client]] == "READY":
        tcp_server.send_msg(client, "Bye " + connections[client])
        del players_statuses[connections[client]]
        del connections[client]
        tcp_server.close_connection(client)
    else:
        tcp_server.send_msg(client, error_msg_prefix + "Can't exit while in a game \n")


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
