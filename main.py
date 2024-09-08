def restock(item, qty):
	if num_items(item) < qty:
		needed = qty - num_items(item)
		for i in range(needed):
			trade(item)

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

# Chess-like grid pattern for planting (true/false instead of white/black).
def chessLikePattern():
	return (get_pos_y() + get_pos_x()) % 2

def main():
	while True:
		# Buy carrot seeds if we don't have any.
		restock(Items.Carrot_Seed, 4)

		# Plant and harvest wood and carrots.
		for y in range(4):
			for x in range(4):
				if get_pos_y() == 3:
					processTile(Grounds.Soil, Entities.Carrots)
				else:
					if chessLikePattern() == 0:
						processTile(Grounds.Turf, Entities.Tree)
					else:
						processTile(Grounds.Turf, Entities.Grass)
				move(East)
			move(South)

main()