# Imports
import socket
import threading
import time

# Creating socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Socket config
host = ''
port = 5050

s.bind((host, port))
s.listen(3)

print("Waiting for players to join")

# Keeping track of players
players = []
playerID = 0
player1 = ""
player2 = ""

# Send data to specific player
def send_to_player(data, currentPlayer):
    for player in players:
        if currentPlayer == player:
            player.sendall(data.encode("utf-8"))

# Send data to players but them self
def send_to_players(data, currentPlayer):
    for player in players:
        if currentPlayer != player:
            player.sendall(data.encode("utf-8"))

# Send data to all players
def send_to_all_players(data):
    for player in players:
        player.send(data.encode("utf-8"))

# Find the winner
def game_handling():
    global player1, player2
    if player1 != "" and player2 != "":
        if player1 == "r":
            if player2 == "r":
                send_to_all_players("IT'S A DRAW!!")
            if player2 == "s":
                send_to_player("You Win!", players[0])
                send_to_player("You Lose!", players[1])
            if player2 == "p":
                send_to_player("You Lose!", players[0])
                send_to_player("You Win!", players[1])
        if player1 == "s":
            if player2 == "s":
                send_to_all_players("IT'S A DRAW!!")
            if player2 == "p":
                send_to_player("You Win!", players[0])
                send_to_player("You Lose!", players[1])
            if player2 == "r":
                send_to_player("You Lose!", players[0])
                send_to_player("You Win!", players[1])
        if player1 == "p":
            if player2 == "p":
                send_to_all_players("IT'S A DRAW!!")
            if player2 == "r":
                send_to_player("You Win!", players[0])
                send_to_player("You Lose!", players[1])
            if player2 == "s":
                send_to_player("You Lose!", players[0])
                send_to_player("You Win!", players[1])
        player1 = ""
        player2 = ""
        # delay sending RESTARTGAME otherwise it will sometimes print it
        time.sleep(0.5)
        send_to_all_players("RESTARTGAME")

# Thread handling
def thread_handling(conn, currentPlayerID):
    while True:
        try:
            dataIn = conn.recv(1024).decode("utf-8")
            global player1, player2
            if dataIn:
                if dataIn == "r" or dataIn == "s" or dataIn == "p":
                    if currentPlayerID == 0:
                        player1 = dataIn
                        game_handling()
                    if currentPlayerID == 1:
                        player2 = dataIn
                        game_handling()
                else:
                    conn.send("\n Not a correct input...".encode("utf-8"))
        except:
            global playerID
            print("Player Disconnected: " + str(currentPlayerID))
            players.pop(currentPlayerID)
            playerID = currentPlayerID
            break

# Handling incoming connections
while True:
    if playerID < 3:
        conn, addr = s.accept()
        print("Player connected from: " + str(addr))
        players.append(conn)

        # Threading
        thread = threading.Thread(target=thread_handling, args=(conn, playerID))
        thread.start()
        
        if len(players) == 2:
            send_to_all_players("READY_TO_PLAY")

        playerID += 1
    else:
        print("Can't have more players...")
        break
