import socket
import threading

host = '192.168.56.103'
port = 8888
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((host, port))
except socket.error as e:
    print(str(e))

print(" Waiting for other player")

def send_data(data):
    client.send(data.encode("utf-8"))

def game():
    i = 0
    while i<5:
        player_choice = str(input("Rock(r) Scissor(s) Paper(p) : "))
        if player_choice == "r" or player_choice == "s" or player_choice == "p":
            send_data(player_choice)
            print("Waiting for other player...")
            game_result = client.recv(1024).decode("utf-8")
            if "READY_TO_PLAY" not in game_result:
                print(game_result)
            else:
                if "You Win!" in game_result:
                    print("You Win!")
                else:
                    print("You Lose!") 
            i+=1 
        else:
            print("Not correct input...")

ready_to_play = False

while True:
    dataIn = client.recv(1024).decode("utf-8")
    if not ready_to_play:
        if dataIn == "READY_TO_PLAY":
            print("Ready to play")
            game()
            ready_to_play = True
    client.close()
    print ("connection closed")
