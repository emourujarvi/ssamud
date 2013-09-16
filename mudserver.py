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

	def broadcast(self, msg):
		"""
		Send msg to every client.
		"""
		for client in self.CLIENTS:
			if client.login:
				client.send(msg)

	def send_prompt(self, player):
		player.client.send("\n> ");

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

		if len(msg) < 1:
			return

		if client.login:

			player = self.WORLD.player_get(client.login)

			if msg[0] == "'" or msg[0:4] == "say ":
				if msg[0] == "'":
					msg = msg[1:]
				else:
					msg = msg[4:]
				print('%s says, "%s"' % (player.name, msg))
				player.on_say('%s says, %s\n' % (player.name, msg))

			elif msg[0] == "-" or msg[0:4] == "com ":
				if msg[0] == "'":
					msg = msg[1:]
				else:
					msg = msg[4:]
				print('%s broadcasts, "%s"' % (player.name, msg))
				self.broadcast('%s broadcasts, %s\n' % (player.name, msg))

			else:
				c = msg.lower()

				if c == 'quit':
					player.client.deactivate()
				elif c == 'n' or c == 'north' or c == 's' or c == 'south' or c == 'e' or c == 'east' or c == 'w' or c == 'west':
					c = c[0]
					player.on_move(c)
				elif c == 'l' or c == 'look':
					player.room.on_look(player)
				elif c == 'exits':
					player.room.on_look_exits(player)
				elif c == 'where':
					player.client.send("You are now in (Roomid " + str(player.room.roomid) + ") " + player.room.name)

			self.send_prompt(player)

		else:
			if re.match("^[A-Za-z]+$", msg):
				client.login = msg
				print("-- %s is now known as %s" % (client.addrport(), client.login))
				# TODO Search if user exists already. Prohibit same names.
				player = self.WORLD.player_login(client, client.login)
				# self.send_room_description(player)
				self.broadcast('\n%s joined the server.\n> ' % client.login )
				# self.send_prompt(client)
			else:
				client.send_cc("^RImproper name. Use only letters.^~\n");
				self.send_login(client);