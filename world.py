from room import Room
from player import Player

class World():

	def __init__(self, rooms = None):
		self.rooms = {}
		self.room_count = 0
		self.players = {}

	def set_rooms(self, rooms):
		self.rooms = rooms

	def room_add(self, room):
		self.room_count = len(self.rooms)
		roomid = self.room_count
		self.rooms[roomid] = room
		room.set_roomid(roomid)
		room.set_parent(self)
		return self.rooms[roomid]

	def room_get(self, rid):
		if self.rooms:
			if self.room_count > rid:
				return self.rooms[rid]
			else:
				raise Exception("No room with id " + str(rid) + " found!\n")
		else:
			raise Exception("No rooms!")

	def player_add(self, client, name, room):
		self.players[name] = Player(client, name, room)
		return self.players[name]

	def player_get(self, name):
		return self.players[name]

	def player_login(self, client, name):
		if name in self.players:
			self.players[name].client = client
			return self.players[name]
		else:
			return self.player_add(client, name, self.room_get(0))