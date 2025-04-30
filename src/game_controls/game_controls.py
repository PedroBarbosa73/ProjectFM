import pyautogui
import time
from config import PAUSE_BUTTON_IMAGE, RESUME_BUTTON_IMAGE

def pause_game():
    """Pauses the game by clicking the pause button or pressing space."""
    print("Attempting to pause the game...")
    
    # First try clicking the pause button
    try:
        pause_location = pyautogui.locateOnScreen(PAUSE_BUTTON_IMAGE, confidence=0.8)
        if pause_location:
            pyautogui.click(pyautogui.center(pause_location))
            print("Game Paused using pause button.")
            return True
    except Exception as e:
        print(f"Error finding pause button: {e}")
    
    # If pause button not found, try pressing space
    try:
        pyautogui.press('space')
        print("Game Paused using space key.")
        return True
    except Exception as e:
        print(f"Error pressing space key: {e}")
    
    print("Failed to pause the game.")
    return False

def resume_game():
    """Resumes the game by clicking the resume button or pressing space."""
    print("Attempting to resume the game...")
    
    # First try clicking the resume button
    try:
        resume_location = pyautogui.locateOnScreen(RESUME_BUTTON_IMAGE, confidence=0.8)
        if resume_location:
            pyautogui.click(pyautogui.center(resume_location))
            print("Game Resumed using resume button.")
            return True
    except Exception as e:
        print(f"Error finding resume button: {e}")
    
    # If resume button not found, try pressing space
    try:
        pyautogui.press('space')
        print("Game Resumed using space key.")
        return True
    except Exception as e:
        print(f"Error pressing space key: {e}")
    
    print("Failed to resume the game.")
    return False 