import socket

UDP_PORT = 61507

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))

POSITIONS = {}
MARKERS = set(['V', 'W', 'X', 'Y', 'Z'])
CURRENT_GOAL = False

def acquire_positions(udp_sock=sock):
	while not MARKERS.issubset(set(POSITIONS.keys())):
		udp_list = udp_sock.recv(1024).split(',')
		POSITIONS.update({marker: grab_loc(udp_list, marker) for marker in MARKERS if grab_loc(udp_list, marker)})
		print POSITIONS

def grab_loc(udp_list, marker):
	try:
		start_index = udp_list.index(marker)
		location = (int(udp_list[start_index+1]), int(udp_list[start_index+2]))
		if location == (-1, -1):
			return False
		return location
	except ValueError:
		return False

def get_robit_position(robit="G", udp_sock=sock):
	position = False
	while not position:
		position = grab_loc(udp_sock.recv(1024).split(','), robit)
	return position

def distance_function(pos1, pos2):
	return sum([(a - b)**2 for a, b in zip(pos1, pos2)])

def set_next_waypoint():
	# If we've never been somewhere before, then grab the top-most waypoint
	# Otherwise just go to the closest one.
	global CURRENT_GOAL
	pos = get_robit_position()
	if CURRENT_GOAL:
		next_goal = min(POSITIONS, key=lambda x: distance_function(POSITIONS.get[x], pos))
	else:
		next_goal = max(POSITIONS, key=lambda x: POSITIONS.get(x)[1])
	CURRENT_GOAL = POSITIONS.pop(next_goal)
	return CURRENT_GOAL

acquire_positions()
print POSITIONS
