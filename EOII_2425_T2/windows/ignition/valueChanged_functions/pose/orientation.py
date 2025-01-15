def valueChanged(tagPath, previousValue, currentValue, initialChange, missedEvents):
	"""
	Fired whenever the current value changes in value or quality.
	"""
	# STEP 1: Needed defines ---------------------------------------------------

	# Declare path to simplify code
	pose_path = "EOII_2425/EOII_2425_T2/pose/"
	
	# STEP 2: Read orientation OPC Tag -----------------------------------------

	raw_orientation = currentValue.value
	
	# STEP 3: Calculate Orientation for Compass --------------------------------
	
	if raw_orientation >= 0.0:
		orientation_for_compasss = 90 - (raw_orientation / 3.0) * 180
	else:
		orientation_for_compasss = 90 + (raw_orientation / -3.0) * 180
	
	# STEP 4: Update Memory Tag ------------------------------------------------

	system.tag.write(
		pose_path + "orientation_for_compass",
		orientation_for_compasss)
		
	### end def valueChanged() ###
	