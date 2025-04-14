import pyautogui
import time
from config import SHOUTS_BUTTON_IMAGE, SHOUT_IMAGES

def trigger_shout(shout):
    """Opens the shout menu and selects the desired shout."""
    print(f"Trying to use shout: {shout}")
    print(f"Looking for shouts menu at: {SHOUTS_BUTTON_IMAGE}")

    # Try with higher confidence levels for the shouts menu
    for confidence in [0.95, 0.9, 0.85]:  # Increased confidence
        try:
            print(f"Trying confidence level: {confidence}")
            shouts_menu_location = pyautogui.locateOnScreen(SHOUTS_BUTTON_IMAGE, confidence=confidence, grayscale=True)
            if shouts_menu_location:
                print(f"Found shouts menu with confidence {confidence}")
                button_center = pyautogui.center(shouts_menu_location)
                print(f"Moving to shouts menu at: {button_center}")
                pyautogui.moveTo(button_center[0], button_center[1], duration=0.2)
                time.sleep(0.2)
                pyautogui.click(button_center[0], button_center[1])
                time.sleep(1)  # Give time for the menu to open

                # Click the selected shout
                shout_image = SHOUT_IMAGES.get(shout)
                if shout_image:
                    print(f"Looking for shout image at: {shout_image}")
                    # Try with higher confidence levels for the shout
                    for shout_confidence in [0.95, 0.9, 0.85]:  # Increased confidence
                        try:
                            print(f"Trying shout confidence level: {shout_confidence}")
                            shout_location = pyautogui.locateOnScreen(shout_image, confidence=shout_confidence, grayscale=True)
                            if shout_location:
                                print(f"Found shout with confidence {shout_confidence}")
                                x, y, width, height = shout_location  # Get bounding box of the text
                                button_x = x + width - 15  # Move slightly to the right of the text
                                button_y = y + height // 2  # Center vertically
                                print(f"Moving to shout button at: ({button_x}, {button_y})")
                                pyautogui.moveTo(button_x, button_y, duration=0.2)
                                time.sleep(0.2)
                                pyautogui.click(button_x, button_y)
                                print(f"Shout executed: {shout}")
                                return True
                        except Exception as e:
                            print(f"Error finding shout with confidence {shout_confidence}: {e}")
                    print(f"Could not find the shout option: {shout}")
                else:
                    print(f"No shout image found for: {shout}")
                break
        except Exception as e:
            print(f"Error finding shouts menu with confidence {confidence}: {e}")
    
    print("Could not find the shouts menu with any confidence level")
    return False 