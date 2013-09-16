from accessible import Accessible

# def on_open(self, player):
#	pass
# def on_close(self, player):
#	pass
# def on_lock(self, player):
#	pass
# def on_unlock(self, player):
#	pass
# def on_use(self, player):
#	pass
# def on_put(self, player, target):
#	pass
# def on_get(self, player):
#	pass
# def on_drop(self, player):
#	pass
# def on_description(self, player):
#	pass


class Exit(Accessible):

	def __init__(self, target, name = None, open0 = True, locked = False):
		self.target = target
		if name == None:
			self.name = target.name
		else:
			self.name = name
		self.open = open0
		self.locked = locked
		self.msg_locked = "The exit is somehow blocked.\n"

	def __str__(self):
		return "\n\t[Exit to (Roomid " + str(self.target.roomid) + ") " + self.target.name + "]"

	def set_parent(self, parent):
		self.parent = parent

	def on_use(self, player):
		return player.on_room_change(self.target)

	def on_look(self, player):
		player.client.send("An exit to " + self.target.name)

class Door(Exit):
	
	def __init__(self, target, name):
		super().__init__(target, name, False, True)
		self.msg_locked = "The door is locked."

	def open(self):
		self.open = True

	def close(self):
		self.open = False

	def lock(self):
		self.locked = True

	def unlock(self):
		self.locked = False

	def on_use(self, player):
		self.parent.on_say_others(player, player.name + " tried to access " + self.name + ".")
		player.client.send(self.msg_locked)
		return self.parent