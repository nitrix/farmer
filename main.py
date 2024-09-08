while True:
	# Buy carrot seeds if we don't have any.
	if num_items(Items.Carrot_Seed) < 3:
		for i in range(3-num_items(Items.Carrot_Seed)):
			trade(Items.Carrot_Seed)

	# Plant and harvest wood and carrots.
	for y in range(3):
		for x in range(3):
			if can_harvest():
				harvest()
			if get_pos_y() == 1:
				plant(Entities.Bush)
			if get_pos_y() == 2:
				if get_ground_type() == Grounds.Turf:
					till()
				plant(Entities.Carrots)
			move(East)
		move(South)