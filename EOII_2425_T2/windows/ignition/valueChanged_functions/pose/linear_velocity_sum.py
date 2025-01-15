def valueChanged(tagPath, previousValue, currentValue, initialChange, missedEvents):
	"""
	Fired whenever the current value changes in value or quality.
	"""
	# STEP 1: Needed defines ---------------------------------------------------
	
	# Declare paths to simplify code
	cmd_vel_path = "EOII_2425/EOII_2425_T2/cmd_vel/"
	linear_velocity_path = "EOII_2425/EOII_2425_T2/pose/linear_velocity_data/"

    # STEP 2: Read the number of times the linear velocity has been updated ----
    
    # The number of times the linear velocity module value has been updated
    # matches the number of messages sent to cmd_vel, since internally when the
    # linear_velocity data is provided in the ROS2 Pose type message, it is
    # calculated from the components of the velocity vectors of cmd_vel
    
    # The frequency at which this data is updated is 0.2 s, a value set in the 
    # turtlesim_pattern_controller.py module
    
    # Actually linear_velocity of Pose is updating at the same time as every
    # other Pose value, but it is updated with repeated values since the
    # frequency of sending pose messages is much faster than that of cmd_vel
    # messages
	
	counter = system.tag.read(
    	cmd_vel_path + "cmd_vel_msg_counter").value
	
	# STEP 3: Update the average velocity if applicable ------------------------

	if counter != 0:
		system.tag.write(
			linear_velocity_path + "linear_velocity_average",
			currentValue.value / counter)
		
	### end def valueChanged() ###
	