def valueChanged(tagPath, previousValue, currentValue, initialChange, missedEvents):
	"""
	Fired whenever the current value changes in value or quality.
	"""
	# STEP 1: Needed defines ---------------------------------------------------

	# Declare paths to simplify code
	pose_path = "EOII_2425/EOII_2425_T2/pose/"
	angular_velocity_path = pose_path + "angular_velocity_data/"
	linear_velocity_path  = pose_path + "linear_velocity_data/"
	
	# STEP 2: If the server has been restarted, reset Memory Tags --------------
	
	if previousValue.value > currentValue.value or currentValue.value == 0:
	
		# Reset Position and Orientation Memory Tags ---------------------------
		
		system.tag.write(
			pose_path + "orientation_for_compass",
			90.0)
		system.tag.write(
			pose_path + "position_x",
			0.0)
		system.tag.write(
			pose_path + "position_y",
			0.0)
		system.tag.write(
			pose_path + "traveled_distance",
			0.0)

		# Reset Linear Velocity Memory Tags ------------------------------------

		system.tag.write(
			linear_velocity_path + "linear_velocity_average",
			0.0)
		system.tag.write(
			linear_velocity_path + "linear_velocity_max",
			0.0)
		system.tag.write(
			linear_velocity_path + "linear_velocity_min",
			10000.0)
		system.tag.write(
			linear_velocity_path + "linear_velocity_sum",
			0.0)

		# Reset Angular Velocity Memory Tags -----------------------------------

		system.tag.write(
			angular_velocity_path + "angular_velocity_average",
			0.0)
		system.tag.write(
			angular_velocity_path + "angular_velocity_max",
			0.0)
		system.tag.write(
			angular_velocity_path + "angular_velocity_min",
			10000.0)
		system.tag.write(
			angular_velocity_path + "angular_velocity_sum",
			0.0)

	### end def valueChanged() ###
	