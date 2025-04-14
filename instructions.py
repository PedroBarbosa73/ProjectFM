import pyautogui
import time
import os
from config import (
    INSTRUCTIONS_MENU_IMAGE, 
    OK_BUTTON_IMAGE, 
    CANCEL_BUTTON_IMAGE, 
    INSTRUCTIONS_IMAGES,
    BASE_IMAGE_DIR,
    IN_POSSESSION_BUTTON_IMAGE,
    IN_TRANSITION_MENU
)

# Cache for button positions
button_positions = {
    'instructions_menu': None,
    'ok_button': None,
    'cancel_button': None
}

def get_cached_position(button_type):
    """Get cached position for a button type"""
    return button_positions.get(button_type)

def update_cached_position(button_type, position):
    """Update cached position for a button type"""
    button_positions[button_type] = position

def find_button_with_cache(button_type, image_path, confidence=0.9):
    """
    Find a button using cached position if available, otherwise search for it
    Returns: (x, y) position or None if not found
    """
    # Try to use cached position first
    cached_pos = get_cached_position(button_type)
    if cached_pos:
        try:
            # Verify the button is still at cached position
            if pyautogui.locateOnScreen(image_path, confidence=confidence, grayscale=True, region=cached_pos):
                return cached_pos
        except:
            pass  # If verification fails, continue to search
    
    # If no cache or verification failed, search for the button
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence, grayscale=True)
        if location:
            # Update cache with new position
            update_cached_position(button_type, location)
            return location
    except Exception as e:
        print(f"Error finding {button_type}: {e}")
    
    return None

def click_cancel_button():
    """Clicks the Cancel button when OK is unavailable"""
    print("OK button unavailable, looking for Cancel button...")
    cancel_button = find_button_with_cache('cancel_button', CANCEL_BUTTON_IMAGE)
    if cancel_button:
        button_center = pyautogui.center(cancel_button)
        pyautogui.click(button_center)
        time.sleep(0.1)
        print("Clicked Cancel button")
        return True
    print("Could not find Cancel button")
    return False

def open_instructions_menu():
    """Opens the instructions menu."""
    print("Opening instructions menu...")
    try:
        menu_location = pyautogui.locateOnScreen(INSTRUCTIONS_MENU_IMAGE, confidence=0.95)
        if menu_location:
            menu_center = pyautogui.center(menu_location)
            pyautogui.click(menu_center)
            print("Instructions menu opened")
            time.sleep(0.5)  # Wait for menu to open
            return True
        else:
            print("Could not find instructions menu")
            return False
    except Exception as e:
        print(f"Error opening instructions menu: {e}")
        return False

def close_instructions_menu():
    """Close the instructions menu by clicking the OK button."""
    try:
        ok_button = pyautogui.locateOnScreen(OK_BUTTON_IMAGE, confidence=0.9)
        if ok_button:
            pyautogui.click(pyautogui.center(ok_button))
            time.sleep(0.5)  # Wait for menu to close
            return True
        return False
    except Exception as e:
        print(f"Error closing instructions menu: {e}")
        return False

def is_instructions_menu_open():
    """Check if the instructions menu is already open."""
    try:
        # Look for either the Out of Possession or In Transition menu which are only visible when instructions menu is open
        from config import OUT_OF_POSSESSION_MENU
        out_of_possession = pyautogui.locateOnScreen(OUT_OF_POSSESSION_MENU, confidence=0.9)
        in_transition = pyautogui.locateOnScreen(IN_TRANSITION_MENU, confidence=0.9)
        if out_of_possession or in_transition:
            print("Instructions menu is already open")
            return True
        return False
    except Exception as e:
        print(f"Error checking if instructions menu is open: {e}")
        return False

def toggle_instruction(instruction):
    """Toggle an instruction on/off."""
    try:
        # Get the image paths for this instruction
        unselected = INSTRUCTIONS_IMAGES[instruction]["unselected"]
        selected = INSTRUCTIONS_IMAGES[instruction]["selected"]
        
        # First try to find the unselected state
        unselected_loc = pyautogui.locateOnScreen(unselected, confidence=0.9)
        if unselected_loc:
            pyautogui.click(pyautogui.center(unselected_loc))
            time.sleep(0.2)
            return True
            
        # If not found, try the selected state
        selected_loc = pyautogui.locateOnScreen(selected, confidence=0.9)
        if selected_loc:
            pyautogui.click(pyautogui.center(selected_loc))
            time.sleep(0.2)
            return True
            
        print(f"Could not find instruction: {instruction}")
        return False
    except Exception as e:
        print(f"Error toggling instruction {instruction}: {e}")
        return False

def apply_instruction(instruction):
    """Applies an instruction in the 'In Possession' screen."""
    print(f"Toggling instruction: {instruction}")
    
    # Add shorter wait time after opening menu
    time.sleep(0.2)  # Reduced from 0.4
    
    success = toggle_instruction(instruction)
    if success:
        time.sleep(0.1)  # Reduced from 0.3
        print(f"DEBUG: Successfully applied instruction {instruction}")
    else:
        print(f"DEBUG: Failed to apply instruction {instruction}")
    return success

def close_instructions_menu_after_commands():
    """Closes the instructions menu after both commands are processed."""
    print("Closing instructions menu now...")
    close_instructions_menu()

def process_instruction_command(command):
    """Process an instruction command by clicking the appropriate option."""
    print(f"Processing instruction command: {command}")
    
    # Wait for menu to stabilize
    time.sleep(0.5)
    
    # Get the instruction images for this command
    instruction_data = INSTRUCTIONS_IMAGES.get(command)
    if not instruction_data:
        print(f"DEBUG: No image data found for instruction: {command}")
        return False
    
    print(f"DEBUG: Looking for instruction images: {instruction_data}")
    
    # Use the existing toggle_instruction function
    success = toggle_instruction(command)
    if success:
        print(f"DEBUG: Successfully toggled instruction: {command}")
        time.sleep(0.2)  # Wait for the instruction to be applied
        return True
    else:
        print(f"DEBUG: Failed to toggle instruction: {command}")
        return False 