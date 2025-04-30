import pyautogui
import time
import os
from config import (
    INSTRUCTIONS_MENU_IMAGE,
    IN_TRANSITION_MENU,
    OK_BUTTON_IMAGE,
    CANCEL_BUTTON_IMAGE,
    IN_TRANSITION_IMAGES
)

def navigate_to_in_transition(menu_already_open=False):
    """Navigate to the In Transition menu."""
    try:
        # If menu is already open, just look for In Transition
        if menu_already_open:
            print("Menu already open, looking for In Transition...")
            # Try with different confidence levels
            for confidence in [0.9, 0.85, 0.8]:
                in_transition = pyautogui.locateOnScreen(IN_TRANSITION_MENU, confidence=confidence)
                if in_transition:
                    print(f"Found In Transition menu with confidence {confidence}")
                    pyautogui.click(pyautogui.center(in_transition))
                    time.sleep(0.5)  # Wait for menu to open
                    return True
            print("Could not find In Transition menu")
            return False
        
        # If menu is not open, open it first
        print("Opening instructions menu...")
        from instructions import open_instructions_menu
        open_instructions_menu()
        time.sleep(1.0)  # Wait for menu to open
        
        # Now look for In Transition
        print("Looking for In Transition menu...")
        for confidence in [0.9, 0.85, 0.8]:
            in_transition = pyautogui.locateOnScreen(IN_TRANSITION_MENU, confidence=confidence)
            if in_transition:
                print(f"Found In Transition menu with confidence {confidence}")
                pyautogui.click(pyautogui.center(in_transition))
                time.sleep(0.5)  # Wait for menu to open
                return True
        print("Could not find In Transition menu")
        return False
        
    except Exception as e:
        print(f"Error navigating to In Transition menu: {e}")
        return False

def close_in_transition_menu():
    """Close the In Transition menu by clicking the OK button."""
    try:
        ok_button = pyautogui.locateOnScreen(OK_BUTTON_IMAGE, confidence=0.9)
        if ok_button:
            pyautogui.click(pyautogui.center(ok_button))
            time.sleep(0.5)  # Wait for menu to close
            return True
        return False
    except Exception as e:
        print(f"Error closing In Transition menu: {e}")
        return False

def toggle_in_transition_instruction(instruction):
    """Toggle an In Transition instruction on/off."""
    try:
        # Get the image paths for this instruction
        instruction_data = IN_TRANSITION_IMAGES.get(instruction)
        if not instruction_data:
            print(f"Instruction '{instruction}' not found in configuration")
            return False

        # Try to find the unselected state first
        unselected_loc = pyautogui.locateOnScreen(instruction_data["unselected"], confidence=0.9)
        if unselected_loc:
            pyautogui.click(pyautogui.center(unselected_loc))
            time.sleep(0.2)
            return True
            
        # If not found, try the selected state
        selected_loc = pyautogui.locateOnScreen(instruction_data["selected"], confidence=0.9)
        if selected_loc:
            pyautogui.click(pyautogui.center(selected_loc))
            time.sleep(0.2)
            return True
            
        # If still not found, try the hover state
        hover_loc = pyautogui.locateOnScreen(instruction_data["hover"], confidence=0.9)
        if hover_loc:
            pyautogui.click(pyautogui.center(hover_loc))
            time.sleep(0.2)
            return True
            
        print(f"Could not find instruction: {instruction}")
        return False
    except Exception as e:
        print(f"Error toggling instruction {instruction}: {e}")
        return False

def apply_in_transition_instruction(instruction):
    """Applies an instruction in the 'In Transition' screen."""
    print(f"Toggling In Transition instruction: {instruction}")
    
    # Add shorter wait time after opening menu
    time.sleep(0.2)
    
    success = toggle_in_transition_instruction(instruction)
    if success:
        time.sleep(0.1)
        print(f"DEBUG: Successfully applied In Transition instruction {instruction}")
    else:
        print(f"DEBUG: Failed to apply In Transition instruction {instruction}")
    return success 