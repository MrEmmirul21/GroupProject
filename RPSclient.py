# Imports library
import socket
import threading

# Create new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Socket config
host = '192.168.170.14'
port = 5050

# Connect to server socket
s.connect((host, port))
print("Connected to server...")

def send_data(data):
    s.send(data.encode("utf-8"))

def game():
    player_choice = str(input("Rock(r) Scissor(s) Paper(p) : "))
    if player_choice == "r" or player_choice == "s" or player_choice == "p":
        send_data(player_choice)
        print("Waiting for other player...")
        game_result = s.recv(1024).decode("utf-8")
        if "RESTARTGAME" and "READY_TO_PLAY" not in game_result:
            print(game_result)
        else:
            if "You Win!" in game_result:
                print("You Win!")
            else:
                print("You Lose!")    
    else:
        print("Not correct input...")
        game()

ready_to_play = False

while True:
    dataIn = s.recv(1024).decode("utf-8")
    if not ready_to_play:
        if dataIn == "READY_TO_PLAY":
            print("Ready to play")
            game()
            ready_to_play = True
    if dataIn == "RESTARTGAME":
        game()
