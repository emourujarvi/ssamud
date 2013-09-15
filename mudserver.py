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
	    client.login = None
	    client.request_wont_echo()
	    
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
	    print("-- Lost connection to %s (%s)" % (client.login, client.addrport()))
	    self.CLIENTS.remove(client)
	    if client.login:
	    	self.broadcast('%s left the server.\n' % client.login )


	def kick_idle(self):
	    """
	    Looks for idle self.CLIENTS and disconnects them by setting active to False.
	    """
	    ## Who hasn't been typing?
	    for client in self.CLIENTS:
	        if client.idle() > self.IDLE_TIMEOUT:
	            print("-- Kicked idle client %s (%s)" % (client.login, client.addrport()))
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


#------------------------------------------------------------------------------------------------#

	def say(self, player, msg):
		others = self.WORLD.room_get_other_players(player)
		if others:
			for o in others:
				o.client.send(msg)

	def broadcast(self, msg):
		"""
		Send msg to every client.
		"""
		for client in self.CLIENTS:
			if client.login:
				client.send(msg)

	def send_room_description(self, player):
		r = self.WORLD.room_get(player.location)
		player.client.send_cc("\n^B" + r.name + "^~\n" + "-"*70 + "\n")
		player.client.send_wrapped(r.description + "\n")
		if r.exits:
			m = "Exits: ["
			for key in r.exits.keys():
				m += " " + key
			m += " ]\n"
			player.client.send_cc(m)
		if r.players:
			m = ""
			for p in r.players:
				if p != player.name:
					m += "^W" + p + "^~ is here.\n"
			player.client.send_cc(m)

	def attempt_room_change(self, player, direction):
		old_room = self.WORLD.room_get(player.location)
		new_room = self.WORLD.player_change_room(player, direction)

		if old_room != new_room:
			for p in old_room.players:
				self.WORLD.player_get(p).client.send(player.name + " left the room.\n")
			for p in new_room.players:
				self.WORLD.player_get(p).client.send(player.name + " arrived to the room.\n")
			self.send_room_description(player)			

	def send_prompt(self, player):
		player.client.send("> ");

#------------------------------------------------------------------------------------------------#

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

			player = self.WORLD.player_get(client.login)

			if msg[0] == "'" or msg[0:4] == "say ":
				if msg[0] == "'":
					msg = msg[1:]
				else:
					msg = msg[4:]
				print('%s says, "%s"' % (player.name, msg))
				self.say(player, '%s says, %s\n' % (player.name, msg))

			elif msg[0] == "-" or msg[0:4] == "com ":
				if msg[0] == "'":
					msg = msg[1:]
				else:
					msg = msg[4:]
				print('%s broadcasts, "%s"' % (player.name, msg))
				self.broadcast('%s broadcasts, %s\n' % (player.name, msg))

			else:
				c = msg.lower()

				if c == 'exit':
					player.client.deactivate()
				elif c == 'n' or c == 'north' or c == 's' or c == 'south' or c == 'e' or c == 'east' or c == 'w' or c == 'west':
					c = c[0]
					self.attempt_room_change(player, c)
				elif c == 'l' or c == 'look':
					self.send_room_description(player)

			self.send_prompt(player)

		else:
			if re.match("^[A-Za-z]+$", msg):
				client.login = msg
				print("-- %s is now known as %s" % (client.addrport(), client.login))
				# TODO Search if user exists already. Prohibit same names.
				player = self.WORLD.player_login(client, client.login)
				self.send_room_description(player)
				self.broadcast('\n%s joined the server.\n> ' % client.login )
				# self.send_prompt(client)
			else:
				client.send_cc("^RImproper name. Use only letters.^~\n");
				self.send_login(client);