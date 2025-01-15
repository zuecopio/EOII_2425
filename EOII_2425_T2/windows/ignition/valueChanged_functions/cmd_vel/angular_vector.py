def valueChanged(tagPath, previousValue, currentValue, initialChange, missedEvents):
	"""
	Fired whenever the current value changes in value or quality.
	"""
	# STEP 1: Needed defines ---------------------------------------------------

	# Declare path to simplify code
	cmd_vel_path = "EOII_2425/EOII_2425_T2/cmd_vel/"
	
	# STEP 2: Update Memory Tags with new OPC Tag values -----------------------
	
	system.tag.write(
		cmd_vel_path + "angular_x",
		currentValue.value[0])
		
	system.tag.write(
		cmd_vel_path + "angular_y",
		currentValue.value[1])
					
	system.tag.write(
		cmd_vel_path + "angular_z",
		currentValue.value[2])
			
	### end def valueChanged() ###
	