while True:
	for y in range(3):
		for x in range(3):
			if can_harvest():
				harvest()
				plant(Entities.Bush)
			move(East)
		move(South)