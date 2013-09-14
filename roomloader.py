from room import Room
from exits import Exit, Door

class RoomLoader():

	def __init__(self, file):
		self.rooms = {}
		self.load_rooms()

	def load_rooms(self):
		r1 = Room("Arrivals", "You have arrived to a shuttle Arrivals area. It is filled with all kinds of boxes and other containers. You see there is a waiting area to the north from here. Perhaps you should go take a look.")
		r2 = Room("Lobby", "Waiting area looks completely empty of personnel. You see an information ^gterminal^~ on the west wall. An important looking security officer is standing at the center of the room.")

		e1 = {}
		e1["n"] = Exit(2, r2.name)

		e2 = {}
		e2["s"] = Exit(1, r1.name)
		e2["n"] = Door(3, "Locked door")
		
		r1.exits = e1
		r2.exits = e2

		self.rooms[1] = r1
		self.rooms[2] = r2
