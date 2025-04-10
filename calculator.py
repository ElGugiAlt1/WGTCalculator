def calculate_angle_factor(angle):
    """
    Calculate the angle factor based on the angle.
    0° -> 1 (horizontal, right side of circle)
    90° -> 0.1 (vertical, top of circle)
    180° -> 1 (horizontal, left side of circle)
    270° -> 0.1 (vertical, bottom of circle)
    
    Parameters:
    angle (float): The angle in degrees.
    
    Returns:
    float: The angle factor.
    """
    # Convert angle to standard position (0-360°)
    normalized_angle = angle % 360
    
    # For each quadrant, calculate the appropriate factor
    if 0 <= normalized_angle <= 90:
        # First quadrant: 0° (1.0) to 90° (0.1)
        factor = 1 - (normalized_angle / 90) * (1 - 0.1)
    elif 90 < normalized_angle <= 180:
        # Second quadrant: 90° (0.1) to 180° (1.0)
        factor = 0.1 + ((normalized_angle - 90) / 90) * (1 - 0.1)
    elif 180 < normalized_angle <= 270:
        # Third quadrant: 180° (1.0) to 270° (0.1)
        factor = 1 - ((normalized_angle - 180) / 90) * (1 - 0.1)
    else:  # 270 < normalized_angle < 360
        # Fourth quadrant: 270° (0.1) to 360°/0° (1.0)
        factor = 0.1 + ((normalized_angle - 270) / 90) * (1 - 0.1)
    
    return factor

def calculate_steps(distance, wind, angle, wind_direction):
    """
    Perform the calculations step by step.
    
    Parameters:
    distance (float): The distance to the target.
    wind (float): The wind factor.
    angle (float): The angle of the shot.
    wind_direction (str): Direction of the wind ('headwind' or 'tailwind').
    
    Returns:
    dict: A dictionary containing all steps and the final adjusted distance.
    """
    results = {}
    
    # Convert inputs to float to ensure calculations work properly
    distance = float(distance)
    wind = float(wind)
    angle = float(angle)
    
    # Step 1: Distance x Wind
    step_1 = distance * wind
    results["step_1"] = {
        "formula": f"{distance} * {wind}",
        "result": step_1
    }
    
    # Get the angle factor
    angle_factor = calculate_angle_factor(angle)
    
    results["angle_factor"] = angle_factor
    
    # Step 2: Divisor / Angle factor
    if wind_direction.lower() == 'tailwind':  # Tailwind: Divisor is 225
        divisor = 225.0
    elif wind_direction.lower() == 'headwind':  # Headwind: Divisor is 180
        divisor = 180.0
    else:
        return {"error": "Invalid wind direction. Please use 'headwind' or 'tailwind'."}
    
    step_2 = divisor / angle_factor
    results["step_2"] = {
        "divisor": divisor,
        "formula": f"{divisor} / {angle_factor:.4f}",
        "result": step_2
    }
    
    # Step 3: Step 1 / Step 2
    step_3 = step_1 / step_2
    results["step_3"] = {
        "formula": f"{step_1:.4f} / {step_2:.4f}",
        "result": step_3
    }
    
    # Step 4: Add or subtract Step 3 from the distance
    adjusted_distance = 0.0  # Initialize with a default value
    
    if wind_direction.lower() == 'headwind':
        adjusted_distance = distance + step_3  # Headwind: Add Step 3
        results["step_4"] = {
            "formula": f"{distance} + {step_3:.4f}",
            "result": adjusted_distance
        }
    elif wind_direction.lower() == 'tailwind':
        adjusted_distance = distance - step_3  # Tailwind: Subtract Step 3
        results["step_4"] = {
            "formula": f"{distance} - {step_3:.4f}",
            "result": adjusted_distance
        }
    
    results["adjusted_distance"] = adjusted_distance
    return results
    