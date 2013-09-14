class Exit():

	def __init__(self, target, name, open0 = True, locked = False):
		self.target = target
		self.name = name
		self.open = open0
		self.locked = locked
		self.msg_locked = "The exit is somehow blocked.\n"



class Door(Exit):
	
	def __init__(self, target, name):
		super().__init__(target, name, False, True)
		self.msg_locked = "The door is locked.\n"

	def open(self):
		self.open = True

	def close(self):
		self.open = False

	def lock(self):
		self.locked = True

	def unlock(self):
		self.locked = False