def valueChanged(tagPath, previousValue, currentValue, initialChange, missedEvents):
	"""
	Fired whenever the current value changes in value or quality.
	"""
	# STEP 1: Needed imports and defines ---------------------------------------
	
	# Needed import to calculate the traveled distance
	from math import sqrt
	
	# Declare path to simplify code
	pose_path = "EOII_2425/EOII_2425_T2/pose/"
	
	# STEP 2: Read position_vector OPC Tag -------------------------------------
	
	# Read previous Turtle Coordinates
	prev_x = previousValue.value[0]
	prev_y = previousValue.value[1]
	
	# Read current Turtle Coordinates
	new_x = currentValue.value[0]
	new_y = currentValue.value[1]
	
	# STEP 3: Calculate Traveled Distance --------------------------------------
	
	# Read previous Traveled Distance
	traveled_distance = system.tag.read(
		pose_path + "traveled_distance").value
	
	# Calculate new approximate Traveled Distance
	traveled_distance = (traveled_distance +
		sqrt((new_x - prev_x)**2 + (new_y - prev_y)**2))
	
	# STEP 4: Update Memory Tags -----------------------------------------------
	
	# Update new Traveled Distance
	system.tag.write(
		pose_path + "traveled_distance",
		traveled_distance)
	
	# Update new x coordinate
	system.tag.write(
		pose_path + "position_x",
		new_x)
	
	# Update new y coordinate
	system.tag.write(
		pose_path + "position_y",
		new_y)
		
	### end def valueChanged() ###
	