while True:
	if can_harvest():
		harvest()
	else:
		move(North)