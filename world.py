from room import Room
from player import Player

class World():

	def __init__(self, rooms):
		self.rooms = rooms
		self.players = {}

	def room_get(self, id):
		return self.rooms[id]

	def room_get_other_players(self, player):
		others = []
		players = self.room_get(player.location).players
		for p in players:
			if p != player.name:
				others.append(p)
		return others

	def player_add(self, client, name, location):
		self.players[name] = Player(client, name, location)
		r = self.room_get(location)
		r.players.append(name)
		return self.players[name]

	def player_get(self, name):
		return self.players[name]

	def player_login(self, client, name):
		if name in self.players:
			self.players[name].client = client
			return self.players[name]
		else:
			return self.player_add(client, name, 1)

	def player_change_room(self, player, direction):
		r = self.room_get(player.location)
		if direction in r.exits:
			exit = r.exits[direction]
			if exit.locked == False:
				if player.name in r.players:
					r.players.remove(player.name)
				else:
					print("!! Player was not in a room!")
				player.location = exit.target
				r = self.room_get(player.location)
				r.players.append(player.name)
			else:
				player.client.send(exit.msg_locked)
		else:
			player.client.send("You can't go that direction.\n")
		return r