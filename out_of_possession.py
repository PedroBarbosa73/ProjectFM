import pyautogui
import time
import os
import traceback
from instructions import click_cancel_button, open_instructions_menu
from config import (
    DEFENSIVE_LINE_POSITIONS,
    ENGAGEMENT_POSITIONS,
    OUT_OF_POSSESSION_MENU,
    OUT_OF_POSSESSION_DIR
)

# Line of Engagement positions and their corresponding image files
ENGAGEMENT_POSITIONS = {
    "high": os.path.join(OUT_OF_POSSESSION_DIR, "high_press_line_engagement.png"),
    "mid": os.path.join(OUT_OF_POSSESSION_DIR, "mid_block_line_engagement.png"),
    "low": os.path.join(OUT_OF_POSSESSION_DIR, "low_block_line_engagement.png")
}

# Defensive Line positions and their corresponding image files
DEFENSIVE_POSITIONS = {
    "much higher": os.path.join(OUT_OF_POSSESSION_DIR, "much_higher_defensive_line.png"),
    "higher": os.path.join(OUT_OF_POSSESSION_DIR, "higher_defensive_line.png"),
    "standard": os.path.join(OUT_OF_POSSESSION_DIR, "standard_defensive_line.png"),
    "lower": os.path.join(OUT_OF_POSSESSION_DIR, "lower_defensive_line.png"),
    "much lower": os.path.join(OUT_OF_POSSESSION_DIR, "much_lower_defensive_line.png")
}

def get_current_engagement_line():
    """
    Detects current line of engagement position
    Returns: "high", "mid", or "low"
    """
    print("Detecting current line of engagement position...")
    time.sleep(0.5)  # Reduced wait time from 1.0 to 0.5
    found_positions = []
    
    for position, image_path in ENGAGEMENT_POSITIONS.items():
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.9)  # Increased confidence from 0.8 to 0.9
            if location:
                print(f"Found {position} marker at: {location}")
                found_positions.append((position, location))
        except Exception as e:
            print(f"Error checking {position} position: {e}")
    
    if not found_positions:
        print("Could not detect any line of engagement positions")
        return None
    
    if len(found_positions) > 1:
        print(f"Warning: Found multiple positions: {[pos[0] for pos in found_positions]}")
        # If multiple positions found, use the one that's currently selected (should be brighter/more visible)
        # Sort by the confidence of the match
        found_positions.sort(key=lambda x: pyautogui.locateOnScreen(ENGAGEMENT_POSITIONS[x[0]], confidence=0.95) is not None, reverse=True)
    
    current_position = found_positions[0][0]
    print(f"Current engagement line position: {current_position}")
    return current_position

def get_current_defensive_line():
    """
    Detects current defensive line position
    Returns: "much higher", "higher", "standard", "lower", or "much lower"
    """
    print("Detecting current defensive line position...")
    time.sleep(0.4)  # Wait for menu to stabilize
    found_positions = []
    
    # Try with different confidence levels
    for confidence in [0.98, 0.95, 0.9]:  # Increased confidence levels
        for position, image_path in DEFENSIVE_POSITIONS.items():
            try:
                print(f"Checking defensive line position: {position} with confidence {confidence}")
                location = pyautogui.locateOnScreen(image_path, confidence=confidence, grayscale=True)
                if location:
                    print(f"Found defensive line marker {position} at confidence {confidence}: {location}")
                    found_positions.append((position, location, confidence))
                else:
                    print(f"Defensive line position {position} not found at confidence {confidence}")
            except Exception as e:
                print(f"Error while checking defensive line position {position}: {str(e)}")
        
        # If we found positions with this confidence, stop trying lower ones
        if found_positions:
            break
    
    if not found_positions:
        print("Could not detect any defensive line positions")
        return None
    
    if len(found_positions) > 1:
        print(f"Found multiple defensive line positions: {[pos[0] for pos in found_positions]}")
        # Sort by confidence level (highest first)
        found_positions.sort(key=lambda x: x[2], reverse=True)
        # If multiple positions found with same confidence, use the one that's currently selected
        # (should be brighter/more visible)
        found_positions.sort(key=lambda x: pyautogui.locateOnScreen(DEFENSIVE_POSITIONS[x[0]], confidence=0.98, grayscale=True) is not None, reverse=True)
    
    current_position = found_positions[0][0]
    print(f"Current defensive line position: {current_position}")
    return current_position

def move_engagement_line_to(target_position):
    """Move the engagement line to the specified position."""
    try:
        print(f"Moving engagement line to: {target_position}")
        
        # Get current position
        current_position = get_current_engagement_line()
        if not current_position:
            print("Could not determine current position")
            return False
            
        # If already at target position, return True
        if current_position == target_position:
            print(f"Already at target position: {target_position}")
            return True
            
        # Find current position marker
        current_marker = pyautogui.locateOnScreen(ENGAGEMENT_POSITIONS[current_position], confidence=0.9)
        if not current_marker:
            print("Could not find current position marker")
            return False
            
        marker_center = pyautogui.center(current_marker)
        print(f"Found current marker at: {marker_center}")
        
        # First move up 6 pixels
        up_x = marker_center.x
        up_y = marker_center.y - 6
        print(f"Moving up to: ({up_x}, {up_y})")
        pyautogui.moveTo(up_x, up_y, duration=0.1)
        time.sleep(0.1)
        
        # Then move right 8 pixels
        target_x = up_x + 8
        target_y = up_y
        print(f"Moving right to: ({target_x}, {target_y})")
        pyautogui.moveTo(target_x, target_y, duration=0.1)
        time.sleep(0.1)
        
        # Determine drag direction
        positions_order = ["low", "mid", "high"]
        current_index = positions_order.index(current_position)
        target_index = positions_order.index(target_position)
        drag_direction = -1 if target_index > current_index else 1
        
        print(f"Starting drag from {current_position} to {target_position}")
        
        # Start the drag
        pyautogui.mouseDown()
        time.sleep(0.1)
        
        # Drag in larger increments for faster movement
        increment = 25  # Increased from 15 to 25 for longer strokes
        max_attempts = 15  # Reduced from 20 since we're moving faster
        attempts = 0
        
        while attempts < max_attempts:
            drag_amount = increment * drag_direction
            pyautogui.moveRel(0, drag_amount, duration=0.3)  # Slower drag movement
            time.sleep(0.2)  # Reduced from 0.4
            
            # Check if we've reached the target position
            try:
                if pyautogui.locateOnScreen(ENGAGEMENT_POSITIONS[target_position], confidence=0.9, grayscale=True):
                    print(f"Found target position: {target_position}")
                    break
            except Exception as e:
                print(f"Error checking position: {e}")
            
            attempts += 1
            print(f"Attempt {attempts}: Continuing drag...")
        
        time.sleep(0.1)
        pyautogui.mouseUp()
        time.sleep(0.1)
        
        # Verify we reached the target
        new_position = get_current_engagement_line()
        success = new_position == target_position
        print(f"Final position check: {'Success' if success else 'Failed'} - Current position: {new_position}")
        return success
        
    except Exception as e:
        print(f"Error moving engagement line: {str(e)}")
        return False

def adjust_engagement_line(command):
    """Adjust the line of engagement based on the command."""
    try:
        print(f"DEBUG: Adjusting engagement line based on command: {command}")
        
        # Determine the target position
        if "high press" in command or "high block" in command:
            target_position = "high"
        elif "mid block" in command or "middle block" in command:
            target_position = "mid"
        elif "low block" in command or "drop deep" in command:
            target_position = "low"
        else:
            print("DEBUG: Could not determine target position")
            return False
            
        print(f"DEBUG: Target position: {target_position}")
        
        # Get current position
        current_position = get_current_engagement_line()
        if not current_position:
            print("DEBUG: Could not determine current position")
            return False
            
        print(f"DEBUG: Current position: {current_position}")
        
        # Calculate movement
        if current_position == target_position:
            print("DEBUG: Already at target position")
            return True
            
        # Move to target position
        if move_engagement_line_to(target_position):
            print(f"DEBUG: Successfully moved to {target_position}")
            return True
            
        print("DEBUG: Failed to move to target position")
        return False
        
    except Exception as e:
        print(f"DEBUG: Error adjusting engagement line: {str(e)}")
        return False

def adjust_defensive_line(command):
    """Adjust the defensive line based on the command."""
    try:
        print(f"DEBUG: Adjusting defensive line based on command: {command}")
        
        # Determine the target position
        if "much higher" in command:
            target_position = "much higher"
        elif "higher" in command:
            target_position = "higher"
        elif "standard" in command or "normal" in command:
            target_position = "standard"
        elif "lower" in command:
            target_position = "lower"
        elif "much lower" in command:
            target_position = "much lower"
        else:
            print("DEBUG: Could not determine target position")
            return False
            
        print(f"DEBUG: Target position: {target_position}")
        
        # Get current position
        current_position = get_current_defensive_line()
        if not current_position:
            print("DEBUG: Could not determine current position")
            return False
            
        print(f"DEBUG: Current position: {current_position}")
        
        # Calculate movement
        if current_position == target_position:
            print("DEBUG: Already at target position")
            return True
            
        # Move to target position
        if move_defensive_line_to(target_position):
            print(f"DEBUG: Successfully moved to {target_position}")
            return True
            
        print("DEBUG: Failed to move to target position")
        return False
        
    except Exception as e:
        print(f"DEBUG: Error adjusting defensive line: {str(e)}")
        return False

def process_defensive_shape_command(command):
    """Process voice commands for defensive shape adjustments."""
    try:
        print(f"DEBUG: Processing defensive shape command: {command}")
        command = command.lower()
        
        # First try defensive line (checking this first to avoid errors with commands like "lower defensive line")
        if any(term in command for term in ["defensive line", "defense", "defence"]):
            if adjust_defensive_line(command):
                print("DEBUG: Successfully adjusted defensive line")
                return True
            return False
            
        # Then try engagement line
        if any(keyword in command for keyword in ["press", "block"]):
            if adjust_engagement_line(command):
                print("DEBUG: Successfully adjusted engagement line")
                return True
            return False
            
        print("DEBUG: No matching defensive shape command found")
        return False
    except Exception as e:
        print(f"DEBUG: Error processing defensive shape command: {str(e)}")
        return False

def navigate_to_out_of_possession(menu_already_open=False):
    """Navigate to the Out of Possession menu."""
    try:
        # If menu is already open, just look for Out of Possession
        if menu_already_open:
            print("Menu already open, looking for Out of Possession...")
            # Try with different confidence levels
            for confidence in [0.9, 0.85, 0.8]:
                out_of_possession = pyautogui.locateOnScreen(OUT_OF_POSSESSION_MENU, confidence=confidence)
                if out_of_possession:
                    print(f"Found Out of Possession menu with confidence {confidence}")
                    pyautogui.click(pyautogui.center(out_of_possession))
                    time.sleep(0.5)  # Wait for menu to open
                    return True
            print("Could not find Out of Possession menu")
            return False
        
        # If menu is not open, open it first
        print("Opening instructions menu...")
        open_instructions_menu()
        time.sleep(1.0)  # Wait for menu to open
        
        # Now look for Out of Possession
        print("Looking for Out of Possession menu...")
        for confidence in [0.9, 0.85, 0.8]:
            out_of_possession = pyautogui.locateOnScreen(OUT_OF_POSSESSION_MENU, confidence=confidence)
            if out_of_possession:
                print(f"Found Out of Possession menu with confidence {confidence}")
                pyautogui.click(pyautogui.center(out_of_possession))
                time.sleep(0.5)  # Wait for menu to open
                return True
        print("Could not find Out of Possession menu")
        return False
        
    except Exception as e:
        print(f"Error navigating to Out of Possession menu: {e}")
        return False 