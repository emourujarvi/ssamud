class Player():
	
	def __init__(self, client, name, room):
		self.client = client
		self.name = name
		self.room = room
		self.room.on_enter(self)

	def on_move(self, direction):
		old = self.room
		if direction in old.exits:
			exit = old.exits[direction]
			new = exit.on_use(self)
			if old.roomid != new.roomid:
				old.on_exit(self)
				new.on_enter(self)
				return True
		else:
			self.client.send("You can't go that direction.\n")
		return False

	def on_room_change(self, room):
		self.room = room
		return self.room

	def on_say(self, msg):
		self.room.on_say(msg)