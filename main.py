# Retock item when qty becomes lower than `low` and trade enough to get to `high`.
def restockItem(item, low, high):
	if num_items(item) < low:
		needed = high - num_items(item)
		trade(item, needed)

def processTile(desiredGroundType, desiredEntity):
	# Desired ground type.
	currentGroundType = get_ground_type()
	if currentGroundType != desiredGroundType:
		if currentGroundType == Grounds.Turf and desiredGroundType == Grounds.Soil:
			till()
		if currentGroundType == Grounds.Soil and desiredGroundType == Grounds.Turf:
			till()

	# Desired entity - harvesting first.
	if can_harvest():
		harvest()

	# Desired entity - planting second.
	plant(desiredEntity)
	
	# Watering
	if get_ground_type() == Grounds.Soil:
		if get_water() < 0.75:
			use_item(Items.Water_Tank)

# Chess-like grid pattern for planting (0/1 instead of white/black).
def chessLikePattern(x, y):
	return (y + x) % 2
	
def restockSeeds():
	# The possible amount of seeds we could try to plant in one full farm swipe.
	low = get_world_size() * get_world_size()
	
	# Trading takes 200 cycles, so let's overstock just in case.
	# high = max(low, 200)
	high = low * 2
	
	restockItem(Items.Carrot_Seed, low, high)
	restockItem(Items.Pumpkin_Seed, low, high)

	# This isn't a very accurate amount, but eventually there are so many tanks cycling that it self-sustains. 
	if num_items(Items.Water_Tank) < high:
		restockItem(Items.Empty_Tank, 100, 200)

def main():
	clear()

	worldSize = get_world_size()
	
	while True:
		restockSeeds()

		# Plant and harvest wood and carrots.
		for y in range(worldSize):
			for x in range(worldSize):
				if get_pos_y() == 6:
					processTile(Grounds.Soil, Entities.Carrots)
				elif get_pos_y() >= 4:
					if chessLikePattern(x, y) == 0:
						processTile(Grounds.Turf, Entities.Tree)
					else:
						processTile(Grounds.Turf, Entities.Grass)
				else:
					processTile(Grounds.Soil, Entities.Pumpkin)
				move(East)
			move(South)

main()