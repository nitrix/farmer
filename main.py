# TODO: Be smarter about the sunflowers to gain the 8x power multiplier for priorizing sunflowers with more petals.
# TODO: Sweep pathing seems inefficient, maybe a task-list and pathfinding by distance?
# TODO: Swap cactus to improve harvest efficiency.
# TODO: Be mindful of companions in mixed zonage to improve yield.
# TODO: Dinosaur/snake mode.
# TODO: Perform automatic unlocks.
# TODO: Mazes (weird subtances, edges, treasure). 1x1 burns through weird&fertilizer.

item_goals = {
	Items.Cactus: 12000,
	Items.Pumpkin: 64000,
	Items.Power: 100,
	Items.Hay: 134000,
	Items.Wood: 5000,
	Items.Carrot: 16000,
	Items.Weird_Substance: 500,
	Items.Gold: 2000,
}

companions = {}
pumpkin_id_left = 0
pumpkin_id_right = 0

def what_to_plant():
	# Forced zoning for pumpkins.
	if num_items(Items.Pumpkin) < item_goals[Items.Pumpkin]:
		if get_pos_x() < 6 and get_pos_y() < 6:
				return Entities.Pumpkin
		
	# Force zoning for cactus.
	if num_items(Items.Cactus) < item_goals[Items.Cactus]:
		if get_pos_x() < 6 and get_pos_y() >= 6:
				return Entities.Cactus

	# Force zoning for maze.
	if num_items(Items.Gold) < item_goals[Items.Gold]:
		if get_pos_x() == get_world_size()-1 and get_pos_y() == get_world_size()-1:
			return Entities.Bush
	
	if num_items(Items.Power) < item_goals[Items.Power]:
		return Entities.Sunflower
	if num_items(Items.Wood) < item_goals[Items.Wood]:
		return Entities.Bush
	if num_items(Items.Carrot) < item_goals[Items.Carrot]:
		return Entities.Carrot

def safe_planting(entity):
	needs_soil = entity in [Entities.Carrot, Entities.Pumpkin, Entities.Sunflower, Entities.Cactus]
	wrong_ground = (needs_soil and get_ground_type() != Grounds.Soil) or (not needs_soil and get_ground_type() == Grounds.Soil)
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

def fertilizing():
	if num_items(Items.Weird_Substance) < item_goals[Items.Weird_Substance]:
		use_item(Items.Fertilizer)

def weirding():
	if get_pos_x() == get_world_size()-1 and get_pos_y() == get_world_size()-1:
		use_item(Items.Weird_Substance, 1)

def process_tile():
	harvesting()
	entity = what_to_plant()
	if entity == None:
		return
	safe_planting(entity)
	fertilizing()
	weirding()

def sweep_with(f):
	while get_pos_y() < get_world_size():
		while get_pos_x() < get_world_size():
			f()
			if get_pos_x() == get_world_size()-1:
				move(East)
				move(North)
				break
			move(East)
		if get_pos_y() == 0:
			break

def process_grass_tile():
	harvest()
	if get_entity_type() != Entities.Grass:
		safe_planting(Entities.Grass)
	entity, pos = get_companion()
	companions[pos] = entity

def process_companion():
	x, y = get_pos_x(), get_pos_y()
	pos = (x, y)
	if y % 2 != 0:
		if pos in companions:
			entity = companions[pos]
			safe_planting(entity)

def do_hay():
	while not can_harvest():
		do_a_flip()
	
	companions = {}

	sweep_with(process_grass_tile)
	sweep_with(process_companion)

def do_others():
	sweep_with(process_tile)

def main_loop():
	mode = "hay"
	last_mode = ""
	
	while 1:
		if num_items(Items.Hay) < item_goals[Items.Hay]:
			mode = "hay"
		else:
			mode = "others"

		if mode != last_mode:
			if last_mode != "":
				clear()
		
			last_mode = mode

		if mode == "hay":
			do_hay()
		elif mode == "others":
			do_others()

main_loop()
