# Imports library
import socket
import threading

# Create new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Socket config
host = '192.168.170.14'
port = 5050
choices = ['R', 'P', 'S', "s", "p", "r"]

# Connect to server socket
s.connect((host, port))
print("Connected to server...")

def send_data(data):
    s.send(data.encode("utf-8"))

def game():
    print(" ██████╗░░█████╗░░█████╗░██╗░░██╗  ██████╗░░█████╗░██████╗░███████╗██████╗░")
    print(" ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝  ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗")
    print(" ██████╔╝██║░░██║██║░░╚═╝█████═╝░  ██████╔╝███████║██████╔╝█████╗░░██████╔╝")
    print(" ██╔══██╗██║░░██║██║░░██╗██╔═██╗░  ██╔═══╝░██╔══██║██╔═══╝░██╔══╝░░██╔══██╗")
    print(" ██║░░██║╚█████╔╝╚█████╔╝██║░╚██╗  ██║░░░░░██║░░██║██║░░░░░███████╗██║░░██║") 
    print(" ╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░╚═╝  ╚═╝░░░░░╚═╝░░╚═╝╚═╝░░░░░╚══════╝╚═╝░░╚═╝")
    print(" ░██████╗░█████╗░██╗░██████╗░██████╗░█████╗░██████╗░")
    print(" ██╔════╝██╔══██╗██║██╔════╝██╔════╝██╔══██╗██╔══██╗")
    print(" ╚█████╗░██║░░╚═╝██║╚█████╗░╚█████╗░██║░░██║██████╔╝")
    print(" ░╚═══██╗██║░░██╗██║░╚═══██╗░╚═══██╗██║░░██║██╔══██╗")
    print(" ██████╔╝╚█████╔╝██║██████╔╝██████╔╝╚█████╔╝██║░░██║")
    print(" ╚═════╝░░╚════╝░╚═╝╚═════╝░╚═════╝░░╚════╝░╚═╝░░╚═╝")
    print(" ###  Welcome to Rock Paper Scissor Multiplayer Game!  ###")
    print(" [R] Rock ")
    print(" [P] Paper ")
    print(" [S] Scissors ")
    player_choice = input("Rock/Paper/Scissors : ")
    
    if player_choice in choices:
        send_data(player_choice)
        print("Waiting for another player to choose")
        game_result = s.recv(1024).decode("utf-8")
        if "RESTARTGAME" and "READY_TO_PLAY" not in game_result:
            print(game_result)
        else:
            if "You Win!" in game_result:
                print("You Win!")
            else:
                print("You Lose!")    
    else:
        print("Error: Invalid input.")
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
