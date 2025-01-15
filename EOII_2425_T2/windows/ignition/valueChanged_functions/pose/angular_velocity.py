def valueChanged(tagPath, previousValue, currentValue, initialChange, missedEvents):
	"""
	Fired whenever the current value changes in value or quality.
	"""
	# STEP 1: Needed defines ---------------------------------------------------

	# Declare paths to simplify code
	angular_velocity_path = "EOII_2425/EOII_2425_T2/pose/angular_velocity_data/"

	# STEP 2: Update the maximum velocity if applicable ------------------------

	if (currentValue.value > system.tag.read(
		angular_velocity_path + "angular_velocity_max").value):
		system.tag.write(
			angular_velocity_path + "angular_velocity_max",
			currentValue.value)
			
	# STEP 3: Update the minimum velocity if applicable ------------------------
	
	if (currentValue.value < system.tag.read(
		angular_velocity_path + "angular_velocity_min").value):
		system.tag.write(
			angular_velocity_path + "angular_velocity_min",
			currentValue.value)
						
	# STEP 4: Increase the total sum of velocity -------------------------------
	
	system.tag.write(
		angular_velocity_path + "angular_velocity_sum",
		system.tag.read(
			angular_velocity_path +
			"angular_velocity_sum").value + currentValue.value)
			
	### end def valueChanged() ###
	