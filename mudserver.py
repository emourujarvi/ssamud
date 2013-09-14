class MudServer():

	def __init__(self):
		self.IDLE_TIMEOUT = 300
		self.CLIENTS = []
		self.SERVER_RUN = False

	def link_telnet(self, telnet):
			self.telnet = telnet
			self.SERVER_RUN = True

	def on_connect(self, client):
	    """
	    Sample on_connect function.
	    Handles new connections.
	    """
	    print("++ Opened connection to %s" % client.addrport())
	    self.broadcast('%s joins the conversation.\n' % client.addrport() )
	    client.send("Welcome to the Chat Server, %s.\n" % client.addrport() )
	    if self.CLIENTS:
	    	client.send("Other online users:\n")
	    	for c in self.CLIENTS:
	    		client.send('%s ' % c.addrport())
	    else:
	    	client.send("No other users online.")
	    client.send('\n')
	    self.CLIENTS.append(client)
	    


	def on_disconnect(self, client):
	    """
	    Sample on_disconnect function.
	    Handles lost connections.
	    """
	    print("-- Lost connection to %s" % client.addrport())
	    self.CLIENTS.remove(client)
	    self.broadcast('%s left the conversation.\n' % client.addrport() )


	def kick_idle(self):
	    """
	    Looks for idle self.CLIENTS and disconnects them by setting active to False.
	    """
	    ## Who hasn't been typing?
	    for client in self.CLIENTS:
	        if client.idle() > self.IDLE_TIMEOUT:
	            print('-- Kicked idle lobby client from %s' % client.addrport())
	            client.active = False


	def process_clients(self):
	    """
	    Check each client, if client.cmd_ready == True then there is a line of
	    input available via client.get_command().
	    """
	    for client in self.CLIENTS:
	        if client.active and client.cmd_ready:
	            ## If the client sends input echo it to the chat room
	            self.chat(client)


	def broadcast(self, msg):
	    """
	    Send msg to every client.
	    """
	    for client in self.CLIENTS:
	        client.send(msg)


	def chat(self, client):
	    """
	    Echo whatever client types to everyone.
	    """
	    msg = client.get_command()
	    print('%s says, "%s"' % (client.addrport(), msg))

	    for guest in self.CLIENTS:
	        if guest != client:
	            guest.send('%s says, %s\n' % (client.addrport(), msg))
	        else:
	            guest.send('You say, %s\n' % msg)

	    cmd = msg.lower()
	    ## bye = disconnect
	    if cmd == 'bye':
	        client.active = False
	    ## shutdown == stop the server
	    elif cmd == 'shutdown':
	        self.SERVER_RUN = False