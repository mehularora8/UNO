# import socket
# import pickle
# from multiprocessing.connection import Client

# class Network():

# 	def __init__(self):

# 		# self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 		self.server = socket.gethostbyname(socket.gethostname())
# 		self.port = 5555
# 		self.client = Client((self.server, self.port))
# 		self.addr = (self.server, self.port)
# 		# which player number are we?
# 		self.playerNumber = self.connect()

# 	def getPlayerNumber(self):
# 		return self.playerNumber

# 	def connect(self):
# 		try: 
# 			return int(self.client.recv(512).decode('utf-8'))
# 		except:
# 			print("Could not connect")

# 	def send(self, data, typeOfData):
# 		"""
# 		Param: type- What type of data are you sending? "C" for command or "M" for move
# 		"""

# 		if typeOfData == "C":
# 			# Sending a command and not a move
# 			try: 
# 				self.client.send(data)
# 				if data != "move":
# 					receivedData = self.client.recv(1024 * 4)
# 					return pickle.loads(receivedData)

# 			except socket.error as e:
# 				print(e)

# 		elif typeOfData == "M":
# 			# Sending a move and not a command
# 			try:
# 				self.client.send(data)
# 				receivedData = self.client.recv(1024 * 4)
# 				return pickle.loads(receivedData)

# 			except socket.error as e:
# 				print(e)