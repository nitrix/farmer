pumpkin_id_left = 0
pumpkin_id_right = 0

def what_to_plant():
	# Forced zoning for pumpkins.
	if num_items(Items.Pumpkin) < 64000:
		if get_pos_x() < 6 and get_pos_y() < 6:
				return Entities.Pumpkin

	if num_items(Items.Power) < 100:
		return Entities.Sunflower
	if num_items(Items.Hay) < 1500:
		return Entities.Grass
	if num_items(Items.Wood) < 300:
		return Entities.Bush
	if num_items(Items.Carrot) < 16000:
		return Entities.Carrot

def needs_soil(entity):
	return entity in [Entities.Carrot, Entities.Pumpkin, Entities.Sunflower]

def planting():
	entity = what_to_plant()
	if entity == None:
		return
	
	wrong_ground = (needs_soil(entity) and get_ground_type() != Grounds.Soil) or (not needs_soil(entity) and get_ground_type() == Grounds.Soil)
	if wrong_ground:
		till()

	plant(entity)

def harvesting_pumpkin():
	global pumpkin_id_left
	global pumpkin_id_right

	if get_entity_type() == Entities.Pumpkin:
		if get_pos_x() == 0:
			pumpkin_id_left = measure()
		if get_pos_x() == 5:
			pumpkin_id_right = measure()

		if pumpkin_id_left == pumpkin_id_right:
			harvest()

def harvesting():
	if can_harvest():
		if get_entity_type() == Entities.Pumpkin:
			harvesting_pumpkin()
		else:
			harvest()

def process_tile():
	harvesting()
	planting()

def infinitely_sweep_board_with(f):
	while 1:
		f()

		x = get_pos_x()

		if x < get_world_size()-1:
			move(East)
		elif x == get_world_size()-1:
			move(East)
			move(North)

#clear()
infinitely_sweep_board_with(process_tile)