class Room():
	
	def __init__(self, name, desc, exits = None):
		self.name = name
		self.description = desc
		self.exits = exits
		self.players = []