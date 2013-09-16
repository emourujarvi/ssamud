from miniboa import TelnetServer
from mudserver import MudServer
from roomloader import RoomLoader
from world import World

#------------------------------------------------------------------------------
#       Main
#------------------------------------------------------------------------------

if __name__ == '__main__':

	world = World()
	roomloader = RoomLoader(world, "rooms.txt")

	server = MudServer(world);
	
	telnet_server = TelnetServer(port=7777, address='', on_connect=server.on_connect, on_disconnect=server.on_disconnect, timeout = .05)
	server.link_telnet(telnet_server)

	print(">> Listening for connections on port %d.  CTRL-C to break." % server.telnet.port)

	while server.SERVER_RUN:
		server.telnet.poll()        ## Send, Recv, and look for new connections
		server.kick_idle()          ## Check for idle clients
		server.process_clients()    ## Check for client input

	print(">> Server shutdown.")