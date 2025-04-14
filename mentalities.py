import pyautogui
import time
from config import MENTALITY_IMAGES, TARGET_MENTALITY_IMAGES

def find_and_click_mentality_menu():
    """Locates and clicks on the current mentality menu."""
    for mentality, image_path in MENTALITY_IMAGES.items():
        try:
            menu_location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            if menu_location:
                menu_center = pyautogui.center(menu_location)
                pyautogui.click(menu_center)
                print(f"Clicked on mentality menu: {mentality}")
                return mentality
        except pyautogui.ImageNotFoundException:
            print(f"Could not find {image_path} on screen.")

    print("Could not find the mentality menu.")
    return None

def change_mentality_to(target_mentality):
    """Changes the mentality by clicking the appropriate option."""
    print(f"Trying to change mentality to: {target_mentality}")

    current_mentality = find_and_click_mentality_menu()

    if current_mentality:
        time.sleep(1)
        target_mentality_image = TARGET_MENTALITY_IMAGES.get(target_mentality)

        if target_mentality_image:
            # Try with different confidence levels
            for confidence in [0.95, 0.9, 0.85]:
                try:
                    print(f"Trying to find target mentality with confidence {confidence}")
                    target_location = pyautogui.locateOnScreen(target_mentality_image, confidence=confidence, grayscale=True)
                    if target_location:
                        target_center = pyautogui.center(target_location)
                        print(f"Moving to target mentality at: {target_center}")
                        pyautogui.moveTo(target_center[0], target_center[1], duration=0.2)
                        time.sleep(0.2)
                        pyautogui.click(target_center[0], target_center[1])
                        print(f"Changed mentality to: {target_mentality}")
                        return True
                except Exception as e:
                    print(f"Error finding target mentality with confidence {confidence}: {e}")
            print(f"Could not find the target mentality option: {target_mentality}")
        else:
            print(f"No target mentality option image found for: {target_mentality}")
    else:
        print("Could not find or click the mentality menu.")
    
    return False 