import pyautogui
import time
import re
import os
import sys
from PIL import Image
from config import (
    SUBSTITUTIONS_MENU_IMAGE, CONFIRM_SUB_BUTTON, 
    SUBSTITUTE_IMAGES, POSITION_BUTTONS,
    INSTRUCTIONS_MENU_IMAGE, POSITION_MAPPINGS
)

def get_screen_info():
    """Get information about the screen resolution and scaling."""
    screen_width, screen_height = pyautogui.size()
    print(f"\nScreen Information:")
    print(f"Screen Resolution: {screen_width}x{screen_height}")
    return screen_width, screen_height

def open_substitution_menu():
    """Opens the substitution menu."""
    print("\n=== Opening Substitution Menu ===")
    print(f"Using image path: {SUBSTITUTIONS_MENU_IMAGE}")
    
    # Get screen information
    screen_width, screen_height = get_screen_info()
    
    # Check if file exists
    if not os.path.exists(SUBSTITUTIONS_MENU_IMAGE):
        print(f"ERROR: Substitution menu image file does not exist at: {SUBSTITUTIONS_MENU_IMAGE}")
        return False
    
    print(f"Image file exists, size: {os.path.getsize(SUBSTITUTIONS_MENU_IMAGE)} bytes")
    
    try:
        # Try with different confidence levels
        for confidence in [0.6, 0.55, 0.5]:  # Lower confidence levels for better detection
            print(f"\nTrying to find substitution menu with confidence {confidence}")
            try:
                # Get the image dimensions
                menu_image = Image.open(SUBSTITUTIONS_MENU_IMAGE)
                print(f"Menu image dimensions: {menu_image.size}")
                
                menu_location = pyautogui.locateOnScreen(SUBSTITUTIONS_MENU_IMAGE, confidence=confidence)
                if menu_location:
                    # Get the center coordinates of the button
                    button_center = pyautogui.center(menu_location)
                    print(f"Found substitution menu at {button_center} with confidence {confidence}")
                    print(f"Menu region: {menu_location}")
                    
                    # Move to the button and click with more precise timing
                    print(f"Moving to {button_center}")
                    pyautogui.moveTo(button_center[0], button_center[1], duration=0.2)
                    time.sleep(0.2)
                    print("Clicking...")
                    pyautogui.click(button_center[0], button_center[1])  # Click at exact coordinates
                    time.sleep(0.5)
                    
                    # Move mouse to a safe position (same x coordinate, but lower y)
                    safe_x = button_center[0]
                    safe_y = button_center[1] + 50  # Move 50 pixels down from the button
                    print(f"Moving mouse to safe position: ({safe_x}, {safe_y})")
                    pyautogui.moveTo(safe_x, safe_y, duration=0.2)
                    
                    print("Opened substitution menu")
                    return True
                else:
                    print(f"Menu not found with confidence {confidence}")
                    print("Trying to capture screen for debugging...")
                    try:
                        screenshot = pyautogui.screenshot()
                        screenshot.save("debug_screenshot.png")
                        print("Saved debug screenshot as debug_screenshot.png")
                    except Exception as e:
                        print(f"Could not save debug screenshot: {e}")
            except Exception as e:
                print(f"Error while trying confidence {confidence}: {e}")
                print(f"Error type: {type(e).__name__}")
                print(f"Error details: {str(e)}")
    except Exception as e:
        print(f"Error opening substitution menu: {e}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {str(e)}")
    
    print("Could not find substitution menu")
    return False

def select_substitute(substitute_number):
    """Selects a substitute player by number (S1-S12) and returns its location."""
    print(f"\n=== Selecting Substitute {substitute_number} ===")
    
    # Convert to string and ensure proper format
    substitute_number = str(substitute_number)
    if not substitute_number.startswith('S'):
        substitute_number = f'S{substitute_number}'
    
    print(f"Looking for substitute {substitute_number}")
    substitute_image = SUBSTITUTE_IMAGES.get(substitute_number)
    if not substitute_image:
        print(f"No image found for substitute {substitute_number}")
        return None
        
    print(f"Using image path: {substitute_image}")
    
    # Check if file exists
    if not os.path.exists(substitute_image):
        print(f"ERROR: File does not exist: {substitute_image}")
        return None
        
    print(f"File exists, size: {os.path.getsize(substitute_image)} bytes")
    
    # Get the image dimensions
    sub_image = Image.open(substitute_image)
    width, height = sub_image.size
    print(f"Substitute image dimensions: {width}x{height}")
    
    # Adjust confidence levels based on image size
    if width < 30 or height < 30:  # For small images
        confidence_levels = [0.4, 0.35, 0.3]  # Lower confidence for small images
    else:
        confidence_levels = [0.6, 0.55, 0.5]  # Normal confidence for larger images
    
    print(f"Using confidence levels: {confidence_levels}")
    
    # Try with adjusted confidence levels
    for confidence in confidence_levels:
        try:
            print(f"\nTrying to find substitute with confidence {confidence}")
            
            # Try to find the image
            substitute_location = pyautogui.locateOnScreen(substitute_image, confidence=confidence)
            if substitute_location:
                # Convert numpy coordinates to regular integers
                substitute_center = pyautogui.center(substitute_location)
                x = int(substitute_center[0])
                y = int(substitute_center[1])
                print(f"Found substitute {substitute_number} at ({x}, {y}) with confidence {confidence}")
                print(f"Substitute region: {substitute_location}")
                
                # Save debug screenshot if found
                try:
                    screenshot = pyautogui.screenshot()
                    screenshot.save(f"debug_screenshot_{substitute_number}.png")
                    print(f"Saved debug screenshot as debug_screenshot_{substitute_number}.png")
                except Exception as e:
                    print(f"Could not save debug screenshot: {e}")
                
                return (x, y)
            else:
                print(f"Substitute {substitute_number} not found with confidence {confidence}")
                # Save debug screenshot if not found
                try:
                    screenshot = pyautogui.screenshot()
                    screenshot.save(f"debug_screenshot_{substitute_number}_not_found.png")
                    print(f"Saved debug screenshot as debug_screenshot_{substitute_number}_not_found.png")
                except Exception as e:
                    print(f"Could not save debug screenshot: {e}")
        except Exception as e:
            print(f"Error finding substitute with confidence {confidence}: {e}")
            print(f"Error type: {type(e).__name__}")
            print(f"Error details: {str(e)}")
    
    print(f"Could not find substitute {substitute_number}")
    return None

def select_position(position):
    """Selects a position on the field."""
    print(f"\n=== Selecting Position {position} ===")
    
    print(f"Looking for position {position}")
    position_image = POSITION_BUTTONS.get(position)
    if not position_image:
        print(f"No image found for position {position}")
        return None
        
    print(f"Using image path: {position_image}")
    
    # Check if file exists
    if not os.path.exists(position_image):
        print(f"ERROR: File does not exist: {position_image}")
        return None
        
    print(f"File exists, size: {os.path.getsize(position_image)} bytes")
    
    # Try with lower confidence levels for better detection
    for confidence in [0.6, 0.55, 0.5]:
        try:
            print(f"\nTrying to find position with confidence {confidence}")
            # Get the image dimensions
            pos_image = Image.open(position_image)
            print(f"Position image dimensions: {pos_image.size}")
            
            position_location = pyautogui.locateOnScreen(position_image, confidence=confidence)
            if position_location:
                # Convert numpy coordinates to regular integers
                position_center = pyautogui.center(position_location)
                x = int(position_center[0])
                y = int(position_center[1])
                print(f"Found position {position} at ({x}, {y}) with confidence {confidence}")
                print(f"Position region: {position_location}")
                return (x, y)
            else:
                print(f"Position {position} not found with confidence {confidence}")
        except Exception as e:
            print(f"Error finding position with confidence {confidence}: {e}")
            print(f"Error type: {type(e).__name__}")
            print(f"Error details: {str(e)}")
    
    print(f"Could not find position {position}")
    return None

def confirm_substitution():
    """Confirms the substitution."""
    print("\n=== Confirming Substitution ===")
    try:
        print(f"Using image path: {CONFIRM_SUB_BUTTON}")
        
        # Check if file exists
        if not os.path.exists(CONFIRM_SUB_BUTTON):
            print(f"ERROR: File does not exist: {CONFIRM_SUB_BUTTON}")
            return False
            
        print(f"File exists, size: {os.path.getsize(CONFIRM_SUB_BUTTON)} bytes")
        
        # Try with lower confidence levels for better detection
        for confidence in [0.6, 0.55, 0.5]:
            print(f"\nTrying to find confirm button with confidence {confidence}")
            try:
                # Get the image dimensions
                confirm_image = Image.open(CONFIRM_SUB_BUTTON)
                print(f"Confirm button image dimensions: {confirm_image.size}")
                
                confirm_location = pyautogui.locateOnScreen(CONFIRM_SUB_BUTTON, confidence=confidence)
                if confirm_location:
                    confirm_center = pyautogui.center(confirm_location)
                    print(f"Found confirm button at {confirm_center} with confidence {confidence}")
                    print(f"Confirm button region: {confirm_location}")
                    pyautogui.click(confirm_center)
                    print("Substitution confirmed")
                    time.sleep(1)  # Wait for confirmation
                    return True
                else:
                    print(f"Could not find confirm button with confidence {confidence}")
            except Exception as e:
                print(f"Error while trying confidence {confidence}: {e}")
                print(f"Error type: {type(e).__name__}")
                print(f"Error details: {str(e)}")
        
        print("Could not find confirm button with any confidence level")
        return False
    except Exception as e:
        print(f"Error confirming substitution: {e}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        return False

def make_substitution(substitute_number, position):
    """Makes a substitution by dragging the substitute to the target position."""
    print(f"Making substitution: {substitute_number} for {position}")
    
    # First, ensure instructions menu is closed
    print("Checking if instructions menu is open...")
    try:
        from instructions import close_instructions_menu
        close_instructions_menu()
        time.sleep(0.5)  # Wait for menu to close
    except Exception as e:
        print(f"Error closing instructions menu: {e}")
    
    # Then open the substitution menu
    print("Attempting to open substitution menu...")
    if not open_substitution_menu():
        print("Failed to open substitution menu")
        return False
    
    # Wait for menu to fully open
    print("Waiting for menu to fully open...")
    time.sleep(2.0)  # Increased wait time to ensure menu is fully open
    
    # Get the locations for both the substitute and the position
    print(f"Looking for substitute {substitute_number}...")
    substitute_loc = select_substitute(substitute_number)
    if not substitute_loc:
        print(f"Failed to find substitute {substitute_number}")
        return False
        
    print(f"Looking for position {position}...")
    position_loc = select_position(position)
    if not position_loc:
        print(f"Failed to find position {position}")
        return False
    
    # Convert numpy coordinates to regular integers
    sub_x = int(substitute_loc[0])
    sub_y = int(substitute_loc[1])
    pos_x = int(position_loc[0])
    pos_y = int(position_loc[1])
    
    # Validate coordinates
    screen_width, screen_height = pyautogui.size()
    print(f"Screen dimensions: {screen_width}x{screen_height}")
    print(f"Substitute coordinates: ({sub_x}, {sub_y})")
    print(f"Position coordinates: ({pos_x}, {pos_y})")
    
    # Check if position is too close to top of screen
    if pos_y < 50:  # If y coordinate is less than 50 pixels from top
        print(f"Warning: Position {position} is too close to top of screen (y={pos_y})")
        return False
    
    # Perform drag and drop with more precise timing and mouse control
    print(f"Starting drag and drop from ({sub_x}, {sub_y}) to ({pos_x}, {pos_y})")
    
    # Move to substitute position
    print(f"Moving to substitute at ({sub_x}, {sub_y})")
    pyautogui.moveTo(sub_x, sub_y, duration=0.3)
    time.sleep(0.5)  # Wait before clicking
    
    # Click and hold
    print("Clicking and holding...")
    pyautogui.mouseDown()
    time.sleep(0.5)  # Hold longer before starting to drag
    
    # Drag to position with a slight offset to avoid top of screen
    target_x = pos_x
    target_y = pos_y + 10  # Add 10 pixels to avoid top of screen
    print(f"Dragging to position ({target_x}, {target_y})")
    pyautogui.moveTo(target_x, target_y, duration=0.5)
    time.sleep(0.5)  # Wait before releasing
    
    # Release mouse button
    print("Releasing mouse button...")
    pyautogui.mouseUp()
    
    # Wait longer for the substitution to register
    print("Waiting for substitution to register...")
    time.sleep(2.0)
    
    # Confirm the substitution
    print("Looking for confirm button...")
    if confirm_substitution():
        print("Substitution completed successfully")
        time.sleep(0.5)  # Wait after confirmation
        return True
    else:
        print("Failed to confirm substitution")
        return False

def process_substitution_command(command):
    """Processes a voice command for substitution."""
    print(f"Processing substitution command: {command}")
    
    try:
        # Extract substitute number
        substitute_match = re.search(r'S?(\d{1,2})', command.upper())
        if not substitute_match:
            print("Could not find substitute number in command")
            return False
        
        substitute_number = f"S{substitute_match.group(1)}"
        print(f"Found substitute number: {substitute_number}")
        
        # Extract position - look for exact position matches and natural position names
        position = None
        command_upper = command.upper()
        valid_positions = {"GK", "DR", "DCR", "DCL", "DL", "MCR", "MC", "MCL", "AMR", "AML", "STC"}
        
        # First check for special cases like "striker"
        if "STRIKER" in command_upper:
            position = "STC"
        else:
            # Then check for regular position matches
            for pos in valid_positions:
                if pos in command_upper:
                    position = pos
                    break
            
            # If no exact match found, try natural position names
            if not position:
                for natural_name, pos_code in POSITION_MAPPINGS.items():
                    if natural_name.upper() in command_upper:
                        position = pos_code
                        break
                
        if not position:
            print("Could not find valid position in command")
            return False
            
        print(f"Found position: {position}")
        
        # Make the substitution
        return make_substitution(substitute_number, position)
        
    except Exception as e:
        print(f"Error processing substitution command: {e}")
        return False 