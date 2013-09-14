import re

class MudServer():

	def __init__(self, world):
		self.IDLE_TIMEOUT = 300
		self.CLIENTS = []
		self.SERVER_RUN = False
		self.WORLD = world

	def link_telnet(self, telnet):
		self.telnet = telnet
		self.SERVER_RUN = True

	def on_connect(self, client):
	    """
	    Sample on_connect function.
	    Handles new connections.
	    """
	    print("++ Opened connection to %s" % client.addrport())
	    #self.broadcast('%s joined the server.\n' % client.addrport() )
	    # client.send("Welcome to the Chat Server, %s.\n" % client.addrport() )
	    client.location = 1
	    client.login = None
	    
	    # self.send_room_description(client)
	    self.send_mud_flash(client)

	    if self.CLIENTS:
	    	client.send("  Online users:\n  ")
	    	for c in self.CLIENTS:
	    		# client.send('%s ' % c.addrport())
	    		client.send('%s ' % c.login)
	    else:
	    	client.send("  No other users online.")
	    client.send('\n')
	    self.CLIENTS.append(client)

	    self.send_login(client)

	def on_disconnect(self, client):
	    """
	    Sample on_disconnect function.
	    Handles lost connections.
	    """
	    print("-- Lost connection to %s" % client.addrport())
	    self.CLIENTS.remove(client)
	    self.broadcast('%s left the server.\n' % client.addrport() )


	def kick_idle(self):
	    """
	    Looks for idle self.CLIENTS and disconnects them by setting active to False.
	    """
	    ## Who hasn't been typing?
	    for client in self.CLIENTS:
	        if client.idle() > self.IDLE_TIMEOUT:
	            print('-- Kicked idle client from %s' % client.addrport())
	            client.active = False


	def process_clients(self):
	    """
	    Check each client, if client.cmd_ready == True then there is a line of
	    input available via client.get_command().
	    """
	    for client in self.CLIENTS:
	        if client.active and client.cmd_ready:
	            ## If the client sends input echo it to the chat room
	            self.interpret(client)


	def broadcast(self, msg):
		"""
		Send msg to every client.
		"""
		for client in self.CLIENTS:
			if client.login:
				client.send(msg)

	def send_room_description(self, client):
		r = self.WORLD.rooms[client.location]
		client.send_cc("\n^B" + r.name + "^~\n" + "-"*70 + "\n")
		client.send_wrapped(r.description + "\n")
		if r.exits:
			m = "Exits: ["
			for key in r.exits.keys():
				m += " " + key
			m += " ]\n"
			client.send_cc(m)

	def attempt_room_change(self, client, direction):
		r = self.WORLD.rooms[client.location]
		if direction in r.exits:
			exit = r.exits[direction]
			if exit.locked == False:
				client.location = exit.target
				self.send_room_description(client)
			else:
				client.send(exit.msg_locked)
		else:
			client.send("You can't go that direction.\n")

	def send_prompt(self, client):
		client.send("> ");

	def send_mud_flash(self, client):
		name = "Space Station Adventure XII"
		client.send("\n  " + (8 + len(name)) * "*")
		client.send("\n  *   " + (len(name) * " ") + "   *")
		client.send("\n  *   " + name              + "   *")
		client.send("\n  *   " + (len(name) * " ") + "   *")
		client.send("\n  " + (8 + len(name)) * "*" + "\n")

	def send_login(self, client):
		client.send("\n  Input username: ");

	def interpret(self, client):
		"""
		Echo whatever client types to everyone.
		"""
		msg = client.get_command()

		if client.login:

			if msg[0] == "'" or msg[0:4] == "say ":

				if msg[0] == "'":
					msg = msg[1:]
				else:
					msg = msg[4:]

				print('%s says, "%s"' % (client.login, msg))

				for guest in self.CLIENTS:
					if guest != client:
						#guest.send('%s says, %s\n' % (client.addrport(), msg))
						guest.send('%s says, %s\n' % (client.login, msg))
					else:
						guest.send('You say, %s\n' % msg)

			c = msg.lower()

			if c == 'exit':
				client.active = False
			elif c == 'n' or c == 'north' or c == 's' or c == 'south' or c == 'e' or c == 'east' or c == 'w' or c == 'west':
				c = c[0]
				self.attempt_room_change(client, c)

			self.send_prompt(client)

		else:
			if re.match("^[A-Za-z]+$", msg):
				client.login = msg
				self.send_room_description(client)
				self.broadcast('\n%s joined the server.\n> ' % client.login )
				# self.send_prompt(client)
			else:
				client.send_cc("^RImproper name. Use only letters.^~\n");
				self.send_login(client);