def valueChanged(tagPath, previousValue, currentValue, initialChange, missedEvents):
	"""
	Fired whenever the current value changes in value or quality.
	"""
	# STEP 1: Needed defines ---------------------------------------------------

	# Declare path to simplify code
	cmd_vel_path = "EOII_2425/EOII_2425_T2/cmd_vel/"
	
	# STEP 2: If the server has been restarted, reset Memory Tags --------------
	
	if previousValue.value > currentValue.value or currentValue.value == 0:
	
		# Reset Linear Velocity Component Memory Tags --------------------------

		system.tag.write(
			cmd_vel_path + "linear_x",
			0.0)
		system.tag.write(
			cmd_vel_path + "linear_y",
			0.0)
		system.tag.write(
			cmd_vel_path + "linear_z",
			0.0)

		# Reset Angular Velocity Component Memory Tags -------------------------

		system.tag.write(
			cmd_vel_path + "angular_x",
			0.0)
		system.tag.write(
			cmd_vel_path + "angular_y",
			0.0)
		system.tag.write(
			cmd_vel_path + "angular_z",
			0.0)
			
	### end def valueChanged() ###
	