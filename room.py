class Room():
	
	def __init__(self, name, desc):
		self.name = name
		self.description = desc
		self.exits = {}
		self.players = {}

	def __str__(self):
		m = ""
		for e in self.exits:
			m += "\n\t" + e + " to (Roomid " + str(self.exits[e].target.roomid) + ") " + self.exits[e].target.name
		return "(Roomid " + str(self.roomid) + ") " + self.name + " with exits " + m + "\n"

	def set_roomid(self, rid):
		self.roomid = rid

	def set_parent(self, parent):
		self.parent = parent

	def add_exit(self, direction, exit):
		self.exits[direction] = exit
		exit.set_parent(self)

	def get_players(self):
		return self.players

	def get_other_players(self, player):
		others = {}
		for o in self.players.values():
			if o != player:
				others[o.name] = o
		return others

	def on_enter(self, player):
		self.on_say(player.name + " arrived to the room.")
		self.players[player.name] = player
		player.location = self.roomid
		self.on_look(player)

	def on_exit(self, player):
		del self.players[player.name]
		self.on_say(player.name + " left the room.")

	def on_say(self, msg):
		for p in self.get_players().values():
			p.client.send(msg + "\n")

	def on_say_others(self, player, msg):
		for o in self.get_other_players(player).values():
			if o != player:
				o.client.send(msg + "\n")

	def on_look(self, player):
		player.client.send_cc("\n\n^B" + self.name + "^~\n" + "-"*70 + "\n")
		player.client.send_wrapped(self.description + "\n")
		if self.exits:
				m = "Exits: ["
				for key in self.exits.keys():
					m += " " + key
				m += " ]\n"
				player.client.send_cc(m)
		others = self.get_other_players(player).values()
		if others:
			m = ""
			for o in others:
				m += "^W" + o.name + "^~ is here.\n"
			player.client.send_cc(m)

	def on_look_exits(self, player):
		if self.exits:
			m = "\nPossible exits: "
			for key in self.exits.keys():
				m += "\n\t " + key + ": " + self.exits[key].name
			m += " \n\n"
			player.client.send_cc(m)
		else:
			player.client.send_cc("No known exits!\n")