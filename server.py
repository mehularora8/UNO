import socket
import sys
import pickle

from _thread import *
from game import Game

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	str(e)

s.listen(2) #We want 2 connections
print("Waiting for a connection, Server Started")

connected = set()
games = dict()
idCount = 0

def client_thread(conn, p, gameId, games):

	global idCount
	conn.send(str.encode(str(p))) # send player number. No pickling needed

	reply = ""
	#User can either send a move, or inform that they've drawn a card. 

	while True:

		try:
			data = conn.recv(4096)

			if gameId in games:
				# Get game for this player
				game = games[gameId]

				if not data:
					print("No data received")
					break

				else:

					if data.decode() == "get":
						reply = game
						conn.sendall(pickle.dumps(reply))

					if data.decode() == "move":
						newMove = conn.recv(2048)

						# This is a move
						move = pickle.loads(newMove)

						# Move will be of type Class
						game.play(p, move)

						games[gameId] = game
						reply = game
						pickled_reply = pickle.dumps(reply)
						print(pickled_reply)
						conn.sendall(pickled_reply)

					if data.decode() == "draw":
						game.draw(p)

						games[gameId] = game
						reply = game
						pickled_reply = pickle.dumps(reply)
						conn.sendall(pickled_reply)
			else:
				print("No game ID found.")
				break

		except:
			print("error")
			break

	try:
		del games[gameId]
	except:
		pass
	idCount -= 1
	conn.close()


while True:
	conn, addr = s.accept()
	print("Connected to:", addr)

	idCount += 1
	p = 0
	gameId = (idCount - 1)//2

	if idCount % 2 == 1:
		games[gameId] = Game(gameId)
		print("Starting new game")
	else:
		games[gameId].ready = True
		p = 1

	start_new_thread(client_thread, (conn, p, gameId, games))
