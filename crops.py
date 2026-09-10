companion_desires = {}

def sweep_board_with(f):
	move_to(0, 0)

	x = 0
	y = 0
	
	while y < get_world_size():
		while x < get_world_size():
			f()

			if get_pos_x() == get_world_size()-1:
				move(North)

			if get_pos_y() == get_world_size()-1:
				move(East)
				move(North)
				return

			move(East)

def move_to(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

def do_hay_tile():
	harvest()
	entity, pos = get_companion()
	companion_desires[pos] = entity

def do_hay_round():
	sweep_board_with(do_hay_tile)
	fix_companions()
	companion_desires = {}

def needs_soil(entity):
	return entity in [Entities.Carrot, Entities.Pumpkin, Entities.Sunflower, Entities.Cactus]

def planting(entity):
	wrong_ground = (needs_soil(entity) and get_ground_type() != Grounds.Soil) or (not needs_soil(entity) and get_ground_type() == Grounds.Soil)
	if wrong_ground:
		till()

	plant(entity)
	 
def fix_companions():
	print("Companion desires: ", len(companion_desires))

	for pos in companion_desires:
		entity = companion_desires[pos]
		(x, y) = pos
		move_to(x, y)
		planting(entity)