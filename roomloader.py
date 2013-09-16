from room import Room
from exits import Exit, Door

class RoomLoader():

	def __init__(self, world, file):
		self.rooms = {}
		self.world = world
		self.load_rooms()

	def load_rooms(self):
		r1 = self.world.room_add(Room("Arrivals", "You have arrived to a shuttle Arrivals area. It is filled with all kinds of boxes and other containers. You see there is a waiting area to the north from here. Perhaps you should go take a look."))
		r2 = self.world.room_add(Room("Lobby", "Waiting area looks completely empty of personnel. You see an information ^gterminal^~ on the west wall. An important looking security officer is standing at the center of the room."))
		r3 = self.world.room_add(Room("Locked room", "Hey, how did you get here!?"))

		r1.add_exit("n", Exit(r2, r2.name))

		r2.add_exit("s", Exit(r1, r1.name))
		r2.add_exit("n", Door(r3, "Locked door"))

		r3.add_exit("s", Exit(r2, r2.name))
		
		# r1.set_exits()
		# self.world.set_rooms(self.rooms)
