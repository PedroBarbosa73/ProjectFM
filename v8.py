import pyautogui
import time
import keyboard
import azure.cognitiveservices.speech as speechsdk
import pytesseract
from PIL import Image
import re
import os
from out_of_possession import process_defensive_shape_command, navigate_to_out_of_possession

# Set the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define the images directory
IMAGES_DIR = r"C:\Users\Pedro Barbosa\Desktop\images"

AZURE_SPEECH_KEY = "5PkPNpEmedkaolUo07EJuH5iQR151yrcsk194DyqM28JMROhCQknJQQJ99BCACYeBjFXJ3w3AAAYACOG6u6s"
AZURE_REGION = "eastus"

def correct_command(command):
    """Corrects common speech recognition errors in commands."""
    # Replace '4' with 'for' in general text
    command = command.replace('4', 'for')
    
    # Special case: replace 'sfor' with 'S4' for substitutions
    command = command.replace('sfor', 'S4')
    
    # Handle other potential substitution number variations
    command = command.replace('s one', 'S1')
    command = command.replace('s two', 'S2')
    command = command.replace('s three', 'S3')
    command = command.replace('s four', 'S4')
    command = command.replace('s five', 'S5')
    command = command.replace('s six', 'S6')
    command = command.replace('s seven', 'S7')
    command = command.replace('s eight', 'S8')
    command = command.replace('s nine', 'S9')
    command = command.replace('s ten', 'S10')
    command = command.replace('s eleven', 'S11')
    command = command.replace('s twelve', 'S12')
    
    return command

ok_button_image = r"C:\Users\Pedro Barbosa\Desktop\images\instructions\ok_button.png"

mentality_images = {
    'attacking': os.path.join(IMAGES_DIR, "mentalities", "current", "attacking_current.png"),
    'balanced': os.path.join(IMAGES_DIR, "mentalities", "current", "balanced_current.png"),
    'defensive': os.path.join(IMAGES_DIR, "mentalities", "current", "defensive_current.png"),
    'very defensive': os.path.join(IMAGES_DIR, "mentalities", "current", "very_defensive_current.png"),
    'positive': os.path.join(IMAGES_DIR, "mentalities", "current", "positive_current.png"),
    'cautious': os.path.join(IMAGES_DIR, "mentalities", "current", "cautious_current.png"),
    'very attacking': os.path.join(IMAGES_DIR, "mentalities", "current", "very_attacking_current.png"),
}

target_mentality_images = {
    'attacking': os.path.join(IMAGES_DIR, "mentalities", "attacking_mentality.png"),
    'balanced': os.path.join(IMAGES_DIR, "mentalities", "Balanced_mentality.png"),
    'defensive': os.path.join(IMAGES_DIR, "mentalities", "defensive_mentality.png"),
    'very defensive': os.path.join(IMAGES_DIR, "mentalities", "Very_defensive_mentality.png"),
    'positive': os.path.join(IMAGES_DIR, "mentalities", "Positive_mentality.png"),
    'cautious': os.path.join(IMAGES_DIR, "mentalities", "cautious_mentality.png"),
    'very attacking': os.path.join(IMAGES_DIR, "mentalities", "Very_attacking_mentality.png"),
}

shouts_button_image = r'C:\Users\Pedro Barbosa\Desktop\images\Shouts\Shouts_menu.png'
shout_images = {
    'encourage': os.path.join(IMAGES_DIR, "Shouts", "encourage.png"),
    'calm down': os.path.join(IMAGES_DIR, "Shouts", "calm_down.png"),
    'focus': os.path.join(IMAGES_DIR, "Shouts", "Focus.png"),
    'fire up': os.path.join(IMAGES_DIR, "Shouts", "fire_up.png"),
    'no pressure': os.path.join(IMAGES_DIR, "Shouts", "no_pressure.png"),
    'demand more': os.path.join(IMAGES_DIR, "Shouts", "demand_more.png"),
    'praise': os.path.join(IMAGES_DIR, "Shouts", "Praise.png"),
    'berate': os.path.join(IMAGES_DIR, "Shouts", "berate.png"),
}

instructions_menu_image = os.path.join(IMAGES_DIR, "instructions", "instructions_menu.png")

submenus = {
    "in possession": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\in_possesion_menu",
    #"in transition": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_transition.png",
    #"out of possession": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\out_of_possession.png"
}

instructions_images = {
    "hit early crosses": {
        "unselected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\hit_early_crosses_un.png",
        "selected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\hit_early_crosses_sel.png"
    },
    "pass into space": {
        "unselected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\pass_into_space_un.png",
        "selected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\pass_into_space_sel.png"
    },
    "shoot on sight": {
        "unselected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\shoot_on_sight_un.png",
        "selected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\shoot_on_sight_sel.png"
    },
    "work ball into box": {
        "unselected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\work_ball_into_box_un.png",
        "selected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\work_ball_into_box_sel.png"
    },
    "be more expressive": {
        "unselected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\be_more_expressive_un.png",
        "selected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\be_more_expressive_sel.png"
    },
    "be more disciplined": {
        "unselected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\be_more_disciplined_un.png",
        "selected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\be_more_disciplined_sel.png"
    },
    "play for set pieces": {
        "unselected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\play_for_set_pieces_un.png",
        "selected": r"C:\Users\Pedro Barbosa\Desktop\images\instructions\in_possession\play_for_set_pieces_sel.png"
    }
}

# Add substitution menu images
substitution_menu_image = os.path.join(IMAGES_DIR, "Substitutions", "substitutions_menu.png")
confirm_sub_button = os.path.join(IMAGES_DIR, "Substitutions", "confirm_sub.png")
substitution_buttons = {
    "S1": os.path.join(IMAGES_DIR, "Substitutions", "S1.png"),
    "S2": os.path.join(IMAGES_DIR, "Substitutions", "S2.png"),
    "S3": os.path.join(IMAGES_DIR, "Substitutions", "S3.png"),
    "S4": os.path.join(IMAGES_DIR, "Substitutions", "S4.png"),
    "S5": os.path.join(IMAGES_DIR, "Substitutions", "S5.png"),
    "S6": os.path.join(IMAGES_DIR, "Substitutions", "S6.png"),
    "S7": os.path.join(IMAGES_DIR, "Substitutions", "S7.png"),
    "S8": os.path.join(IMAGES_DIR, "Substitutions", "S8.png"),
    "S9": os.path.join(IMAGES_DIR, "Substitutions", "S9.png"),
    "S10": os.path.join(IMAGES_DIR, "Substitutions", "S10.png"),
    "S11": os.path.join(IMAGES_DIR, "Substitutions", "S11.png"),
    "S12": os.path.join(IMAGES_DIR, "Substitutions", "S12.png")
}

position_buttons = {
    'GK': os.path.join(IMAGES_DIR, "Substitutions", "positions", "GK.png"),
    'DR': os.path.join(IMAGES_DIR, "Substitutions", "positions", "DR.png"),
    'DCR': os.path.join(IMAGES_DIR, "Substitutions", "positions", "DCR.png"),
    'DCL': os.path.join(IMAGES_DIR, "Substitutions", "positions", "DCL.png"),
    'DL': os.path.join(IMAGES_DIR, "Substitutions", "positions", "DL.png"),
    'MCR': os.path.join(IMAGES_DIR, "Substitutions", "positions", "MCR.png"),
    'MC': os.path.join(IMAGES_DIR, "Substitutions", "positions", "MC.png"),
    'MCL': os.path.join(IMAGES_DIR, "Substitutions", "positions", "MCL.png"),
    'AMR': os.path.join(IMAGES_DIR, "Substitutions", "positions", "AMR.png"),
    'AML': os.path.join(IMAGES_DIR, "Substitutions", "positions", "AML.png"),
    'STC': os.path.join(IMAGES_DIR, "Substitutions", "positions", "STC.png")
}

# Add pause button image
pause_button_image = r"C:\Users\Pedro Barbosa\Desktop\images\pause.png"

def find_and_click_mentality_menu():
    """Locates and clicks on the current mentality menu."""
    for mentality, image_path in mentality_images.items():
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
        target_mentality_image = target_mentality_images.get(target_mentality)

        if target_mentality_image:
            target_location = pyautogui.locateOnScreen(target_mentality_image, confidence=0.95)
            if target_location:
                target_center = pyautogui.center(target_location)
                pyautogui.click(target_center)
                print(f"Changed mentality to: {target_mentality}")
            else:
                print(f"Could not find the target mentality option: {target_mentality}")
        else:
            print(f"No target mentality option image found for: {target_mentality}")
    else:
        print("Could not find or click the mentality menu.")

def trigger_shout(shout):
    """Opens the shout menu and selects the desired shout."""
    print(f"Trying to use shout: {shout}")
    print(f"Looking for shouts menu at: {shouts_button_image}")

    # Try with higher confidence levels for the shouts menu
    for confidence in [0.95, 0.9, 0.85]:  # Increased confidence
        try:
            print(f"Trying confidence level: {confidence}")
            shouts_menu_location = pyautogui.locateOnScreen(shouts_button_image, confidence=confidence)
    if shouts_menu_location:
                print(f"Found shouts menu with confidence {confidence}")
        pyautogui.click(pyautogui.center(shouts_menu_location))
        time.sleep(1)  # Give time for the menu to open

        # Click the selected shout
        shout_image = shout_images.get(shout)
        if shout_image:
                    print(f"Looking for shout image at: {shout_image}")
                    # Try with higher confidence levels for the shout
                    for shout_confidence in [0.95, 0.9, 0.85]:  # Increased confidence
                        try:
                            print(f"Trying shout confidence level: {shout_confidence}")
                            shout_location = pyautogui.locateOnScreen(shout_image, confidence=shout_confidence)
            if shout_location:
                                print(f"Found shout with confidence {shout_confidence}")
                                x, y, width, height = shout_location
                                # Restore original working click position
                button_x = x + width - 15  # Move slightly to the right of the text
                                button_y = y + height // 2  # Center vertically
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

def pause_game():
    """Pauses the game by clicking the pause button or pressing space."""
    print("Attempting to pause the game...")
    
    # First try clicking the pause button
    try:
        pause_location = pyautogui.locateOnScreen(pause_button_image, confidence=0.8)
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
        resume_location = pyautogui.locateOnScreen(resume_button_image, confidence=0.8)
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

def open_instructions_menu():
    """Finds and clicks the instructions menu."""
    print("Looking for instructions menu...")  # Debug output
    menu_location = pyautogui.locateOnScreen(instructions_menu_image, confidence=0.7)
    if menu_location:
        print("Instructions menu found.")  # Debug output
        pyautogui.click(pyautogui.center(menu_location))
        time.sleep(0.2)  # Added to avoid fast execution errors
        print("Opened Instructions menu.")
        return True
    print("Instructions menu not found.")
    return False

def apply_instruction(instruction):
    """Applies an instruction in the 'In Possession' screen."""
    print(f"Toggling instruction: {instruction}")
    toggle_instruction(instruction)
    time.sleep(0.3)  # Allow time for the instruction to take effect

def toggle_instruction(instruction):
    """Toggles an instruction based on its current state (selected or unselected)."""
    print(f"Toggling instruction: {instruction}")  # Debug output
    instruction_data = instructions_images.get(instruction)
    if not instruction_data:
        print(f"Instruction '{instruction}' not recognized.")  # Debug output
        return

    try:
        # Try with different confidence levels for finding the instruction
        for confidence in [0.7, 0.6, 0.5]:  # Increased confidence levels
            try:
                selected_location = pyautogui.locateOnScreen(instruction_data["selected"], confidence=confidence)
    if selected_location:
        print(f"Instruction '{instruction}' is already selected. Clicking to disable.")  # Debug output
        pyautogui.click(pyautogui.center(selected_location))
        return
            except pyautogui.ImageNotFoundException:
                pass  # Continue to next confidence level

            try:
                unselected_location = pyautogui.locateOnScreen(instruction_data["unselected"], confidence=confidence)
    if unselected_location:
        print(f"Instruction '{instruction}' is not selected. Clicking to enable.")  # Debug output
        pyautogui.click(pyautogui.center(unselected_location))
                    
                    # Special handling for be more expressive and be more disciplined
                    if instruction in ["be more expressive", "be more disciplined"]:
                        # Move mouse to center of screen to avoid info window
                        screen_width, screen_height = pyautogui.size()
                        center_x = screen_width // 2
                        center_y = screen_height // 2
                        pyautogui.moveTo(center_x, center_y)
                        time.sleep(0.2)  # Reduced from 0.5 to 0.2
                        print(f"Info window appeared for {instruction}, mouse moved to center")
        return
            except pyautogui.ImageNotFoundException:
                pass  # Continue to next confidence level

        print(f"Could not find the instruction '{instruction}' on screen with any confidence level.")  # Debug output
    except Exception as e:
        print(f"Error while toggling instruction '{instruction}': {e}")

def close_instructions_menu():
    print("Looking for the OK button to close the menu...")

    time.sleep(0.5)  # Increased delay for menu transitions

    try:
        # Check if we're dealing with be more expressive or be more disciplined
        if any(instruction in pyautogui.getActiveWindow().title.lower() for instruction in ["be more expressive", "be more disciplined"]):
            # Move mouse to center of screen to avoid info window
            screen_width, screen_height = pyautogui.size()
            center_x = screen_width // 2
            center_y = screen_height // 2
            pyautogui.moveTo(center_x, center_y)
            time.sleep(0.2)  # Reduced from 0.5 to 0.2
            print("Moving mouse to center for info window")

        # Now try to find and click the OK button
        ok_button_location = pyautogui.locateOnScreen(ok_button_image, confidence=0.8)
        if ok_button_location:
            ok_button_center = pyautogui.center(ok_button_location)
            pyautogui.click(ok_button_center)
            print("OK button clicked. Instructions menu closed.")
        else:
            print("Could not find the OK button on the screen.")
    except Exception as e:
        print(f"Error in finding the OK button: {e}")


def close_instructions_menu_after_commands():
    """Closes the instructions menu after both commands are processed."""
    print("Closing instructions menu now...")
    close_instructions_menu()

def listen_for_command():
    """Listen for voice command with a 10-second timeout."""
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
    
    # Configure speech recognition settings with longer timeouts
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "3000")  # 3 seconds of silence to end
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "10000")  # 10 seconds to start speaking
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_RequestSentenceBoundary, "true")
    
    # Create speech recognizer with the configured settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Listening for command... (You have 10 seconds to start speaking)")
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        command = result.text.lower()
        print(f"Recognized command: {command}")

        # Correct the command by replacing 4 with 'for'
        command = correct_command(command)

        print(f"Corrected command: {command}")  # Debug output
        return command
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech recognized. Please try again.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Speech recognition canceled.")
    
    return None

def read_positions_and_roles():
    """Reads positions and roles from the game screen using OCR."""
    try:
        # Take a screenshot of the game window
        screenshot = pyautogui.screenshot()
        image_width, image_height = screenshot.size

        # Define the region of interest (ROI)
        start_x, start_y = 700, 183
        width = 130
        height = image_height - start_y

        roi = (start_x, start_y, start_x + width, start_y + height)
        cropped_image = screenshot.crop(roi)

        # Resize the image for better accuracy
        new_width = cropped_image.width * 3
        new_height = cropped_image.height * 3
        cropped_image = cropped_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert to grayscale
        cropped_image = cropped_image.convert('L')

        # Perform OCR
        ocr_output = pytesseract.image_to_string(cropped_image, config='--oem 3 --psm 11', lang='eng')
        ocr_output = ocr_output.replace('$', 'S')

        # Define valid roles
        valid_roles = {"GK", "DR", "DCR", "DCL", "DL", "MCR", "MC", "MCL", "AMR", "AML", "STC"}
        
        # Process the output
        filtered_words = []
        s_items = []
        valid_role_count = 0

        for word in ocr_output.split():
            word_upper = word.upper()
            
            if word_upper in valid_roles:
                filtered_words.append(word_upper)
                valid_role_count += 1
            elif valid_role_count >= 11:
                s_items_pattern = r'\bS[1-9]|S1[0-2]\b'
                if re.match(s_items_pattern, word_upper):
                    s_items.append(word_upper)

        return {
            "roles": " ".join(filtered_words),
            "s_items": " ".join(s_items)
        }
    except Exception as e:
        print(f"Error in OCR processing: {e}")
        return None

def save_positions_to_file(positions_data):
    """Saves the positions and roles data to a file."""
    if positions_data:
        with open('position_role_output.txt', 'w') as file:
            file.write(f"Filtered Roles: {positions_data['roles']}\n")
            file.write(f"S Items: {positions_data['s_items']}\n")
        print("Positions and roles saved to 'position_role_output.txt'")

def open_substitution_menu():
    """Opens the substitution menu."""
    print("Looking for substitution menu...")
    print(f"Using image path: {substitution_menu_image}")
    
    try:
        # Try with different confidence levels
        for confidence in [0.75, 0.7, 0.65]:  # Lower confidence levels
            print(f"Trying to find substitution menu with confidence {confidence}")
            try:
                menu_location = pyautogui.locateOnScreen(substitution_menu_image, confidence=confidence)
                if menu_location:
                    # Get the center coordinates of the button
                    button_center = pyautogui.center(menu_location)
                    print(f"Found substitution menu at {button_center} with confidence {confidence}")
                    
                    # Move to the button and click with more precise timing
                    print(f"Moving to {button_center}")
                    pyautogui.moveTo(button_center[0], button_center[1], duration=0.2)
                    time.sleep(0.2)
                    print("Clicking...")
                    pyautogui.click(button_center[0], button_center[1])  # Click at exact coordinates
                    time.sleep(0.5)
                    print("Opened substitution menu")
                    return True
                else:
                    print(f"Menu not found with confidence {confidence}")
            except Exception as e:
                print(f"Error while trying confidence {confidence}: {e}")
    except Exception as e:
        print(f"Error opening substitution menu: {e}")
    
    print("Could not find substitution menu")
    return False

def select_substitute(substitute_number):
    """Selects a substitute player by number (S1-S12) and returns its location."""
    print(f"Looking for substitute {substitute_number}")
    substitute_image = substitution_buttons.get(substitute_number.upper())  # Make sure to use uppercase
    if not substitute_image:
        print(f"No image found for substitute {substitute_number}")
        return None
        
    print(f"Using image path: {substitute_image}")
    
    # Check if file exists
    if not os.path.exists(substitute_image):
        print(f"ERROR: File does not exist: {substitute_image}")
        return None
        
    print(f"File exists, trying to read it...")
    
    # Try with higher confidence levels
    for confidence in [0.95, 0.9, 0.85]:
        try:
            print(f"Trying to find substitute with confidence {confidence}")
            substitute_location = pyautogui.locateOnScreen(substitute_image, confidence=confidence)
            if substitute_location:
                substitute_center = pyautogui.center(substitute_location)
                print(f"Found substitute {substitute_number} at {substitute_center} with confidence {confidence}")
                return substitute_center
        except Exception as e:
            print(f"Error finding substitute with confidence {confidence}: {e}")
    
    print(f"Could not find substitute {substitute_number}")
    return None

def select_position(position):
    """Selects a position to substitute into and returns its location."""
    print(f"Selecting position {position}")
    position_image = position_buttons.get(position)
    if not position_image:
        print(f"No image found for position {position}")
        return None
        
    print(f"Using image path: {position_image}")
    
    # Try with higher confidence levels for positions
    for confidence in [0.95, 0.9, 0.85]:  # Increased confidence levels
        try:
            print(f"Trying to find position with confidence {confidence}")
            position_location = pyautogui.locateOnScreen(position_image, confidence=confidence)
            if position_location:
                position_center = pyautogui.center(position_location)
                print(f"Found position {position} at {position_center} with confidence {confidence}")
                return position_center
            else:
                print(f"Position not found with confidence {confidence}")
        except Exception as e:
            print(f"Error finding position with confidence {confidence}: {e}")
    
    print(f"Could not find position {position} with any confidence level")
    return None

def confirm_substitution():
    """Clicks the confirm substitution button."""
    print("Looking for confirm substitution button...")
    
    # Try with different confidence levels
    for confidence in [0.8, 0.7, 0.6]:
        try:
            confirm_location = pyautogui.locateOnScreen(confirm_sub_button, confidence=confidence)
            if confirm_location:
                print(f"Found confirm button with confidence {confidence}")
                confirm_center = pyautogui.center(confirm_location)
                pyautogui.click(confirm_center)
                time.sleep(0.5)
                print("Confirmed substitution")
                return True
        except Exception as e:
            print(f"Error finding confirm button with confidence {confidence}: {e}")
    
    print("Could not find confirm substitution button with any confidence level")
    return False

def make_substitution(substitute_number, position):
    """Makes a substitution by dragging the substitute to the target position."""
    print(f"Making substitution: {substitute_number} for {position}")
    
    # First, open the substitution menu
    print("Attempting to open substitution menu...")
    if not open_substitution_menu():
        print("Failed to open substitution menu")
        return False
    
    # Wait for menu to fully open
    print("Waiting for menu to fully open...")
    time.sleep(1)
    
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
    
    # Perform drag and drop
    print(f"Starting drag and drop from {substitute_loc} to {position_loc}")
    pyautogui.moveTo(substitute_loc[0], substitute_loc[1])
    time.sleep(0.2)  # Small delay before starting drag
    pyautogui.mouseDown()
    time.sleep(0.2)  # Hold the mouse button
    pyautogui.moveTo(position_loc[0], position_loc[1], duration=0.5)  # Move to target position
    time.sleep(0.2)  # Small delay before releasing
    pyautogui.mouseUp()
    
    # Wait for the substitution to register
    print("Waiting for substitution to register...")
    time.sleep(1)
    
    # Confirm the substitution
    print("Looking for confirm button...")
    if confirm_substitution():
        print("Substitution completed successfully")
        return True
    else:
        print("Failed to confirm substitution")
        return False

def process_substitution_command(command):
    """Processes a voice command for substitution."""
    print(f"Processing substitution command: {command}")
    
    try:
        # Extract substitute number
        substitute_match = re.search(r'S(\d{1,2})', command.upper())
        if not substitute_match:
            print("Could not find substitute number in command")
            return False
        
        substitute_number = f"S{substitute_match.group(1)}"
        print(f"Found substitute number: {substitute_number}")
        
        # Extract position - look for exact position matches
        valid_positions = {"GK", "DR", "DCR", "DCL", "DL", "MCR", "MC", "MCL", "AMR", "AML", "STC"}
        position = None
        
        # First try to find exact position matches
        for pos in valid_positions:
            if pos in command.upper():
                position = pos
                print(f"Found exact position match: {position}")
                break
        
        # If no exact match found, try to find partial matches
        if not position:
            for pos in valid_positions:
                if pos[:2] in command.upper():  # Check first two letters
                    position = pos
                    print(f"Found partial position match: {position}")
                    break
        
        if not position:
            print("Could not find valid position in command")
            return False
        
        print(f"Attempting substitution: {substitute_number} for {position}")
        return make_substitution(substitute_number, position)
    
    except Exception as e:
        print(f"Error processing substitution command: {e}")
        return False

def process_command(cmd):
    """Process a single command."""
    cmd = cmd.lower()
    
    # Check for defensive shape commands first
    defensive_shape_keywords = [
        "high press", "mid block", "low block",
        "defensive line", "higher defense", "lower defense",
        "much higher", "much lower", "standard defense"
    ]
    
    if any(keyword in cmd for keyword in defensive_shape_keywords):
        if not menu_open:
            if open_instructions_menu():
                menu_open = True
                time.sleep(0.5)
                if navigate_to_out_of_possession():
                    process_defensive_shape_command(cmd)
                    time.sleep(0.5)
                    close_instructions_menu()
                    menu_open = False
                else:
                    print("Failed to navigate to Out of Possession menu")
                    close_instructions_menu()
                    menu_open = False
        else:
            # If menu is already open, just navigate and process
            if navigate_to_out_of_possession():
                process_defensive_shape_command(cmd)
                time.sleep(0.5)
                close_instructions_menu()
                menu_open = False
            else:
                print("Failed to navigate to Out of Possession menu")
                close_instructions_menu()
                menu_open = False
        return

    # Rest of your existing command processing...
    # (mentalities, shouts, instructions, substitutions)

def main():
    print("Hold Caps Lock to activate voice commands.")
    print("Press 'P' to read positions and roles.")
    print("Press 'Space' to pause/resume the game.")
    menu_open = False  
    instructions_applied = 0  
    p_key_pressed = False  # Track if P key is currently pressed
    space_key_pressed = False  # Track if Space key is currently pressed
    last_instruction = None  # Track the last instruction processed

    while True:
        # Check for position reading command
        if keyboard.is_pressed('p') and not p_key_pressed:
            p_key_pressed = True
            print("Reading positions and roles...")
            positions_data = read_positions_and_roles()
            if positions_data:
                save_positions_to_file(positions_data)
            time.sleep(0.5)  # Prevent multiple readings
        elif not keyboard.is_pressed('p'):
            p_key_pressed = False  # Reset when key is released

        # Check for pause/resume command
        if keyboard.is_pressed('space') and not space_key_pressed:
            space_key_pressed = True
            # Try to resume first, if that fails, try to pause
            if not resume_game():
                pause_game()
            time.sleep(0.5)  # Prevent multiple triggers
        elif not keyboard.is_pressed('space'):
            space_key_pressed = False  # Reset when key is released

        # Voice command system
        if keyboard.is_pressed('caps lock'):
            print("Caps Lock held. Speak your command...")
            command = listen_for_command()  

            if command:
                print(f"Captured command: {command}")  
                command = correct_command(command)

                # Split command into individual commands
                commands = command.split('.')
                
                for cmd in commands:
                    cmd = cmd.strip()
                    if not cmd:
                        continue
                        
                    print(f"Processing command: {cmd}")

                    # Check for pause/resume command first
                    if "pause" in cmd.lower():
                        pause_game()
                    elif "resume" in cmd.lower():
                        resume_game()
                    else:
                        # Process each command independently
                        
                        # 1. Check for mentalities
                mentalities = [
                    "very defensive", "very attacking", "attacking", "balanced", 
                    "defensive", "positive", "cautious"
                ]
                for mentality in mentalities:
                            if mentality in cmd:
                        change_mentality_to(mentality)
                                time.sleep(0.5)
                        break  

                        # 2. Check for shouts
                shouts = [
                    "encourage", "calm down", "focus", "fire up", "no pressure", 
                    "demand more", "praise", "berate"
                ]
                for shout in shouts:
                            if shout in cmd:
                        trigger_shout(shout)
                                time.sleep(0.5)
                                break
                        
                        # 3. Check for instructions
                        instruction_variations = {
                            "hit early crosses": ["hit early crosses"],
                            "pass into space": ["pass into space", "passing to space", "pass to space"],
                            "shoot on sight": ["shoot on sight"],
                            "work ball into box": ["work ball into box", "work the ball into box"],
                            "be more expressive": ["be more expressive"],
                            "be more disciplined": ["be more disciplined"],
                            "play for set pieces": ["play for set pieces"]
                        }
                        
                        found_instructions = []
                        for instruction, variations in instruction_variations.items():
                            for variation in variations:
                                if variation in cmd:
                                    found_instructions.append(instruction)
                                    break
                        
                        # Process found instructions
                        if found_instructions:
                if not menu_open:
                    if open_instructions_menu():
                        menu_open = True  
                        time.sleep(0.5)  

                            for instruction in found_instructions:
                            apply_instruction(instruction)
                            instructions_applied += 1 
                                last_instruction = instruction
                                
                                if instruction in ["be more expressive", "be more disciplined"]:
                                    screen_width, screen_height = pyautogui.size()
                                    center_x = screen_width // 2
                                    center_y = screen_height // 2
                                    pyautogui.moveTo(center_x, center_y)
                                    time.sleep(0.2)
                                    print(f"Moving mouse to center for {instruction}")
                                
                                time.sleep(0.5)
                            
                            if last_instruction in ["be more expressive", "be more disciplined"]:
                                time.sleep(0.2)
                            close_instructions_menu_after_commands()
                            menu_open = False
                            instructions_applied = 0
                            last_instruction = None
                        
                        # 4. Check for substitutions
                        if "change" in cmd.lower() and "with" in cmd.lower():
                            print("Processing substitution command...")
                            # Extract the substitute number and position from the command
                            substitute_match = re.search(r'S(\d{1,2})', cmd.upper())
                            if substitute_match:
                                substitute_number = f"S{substitute_match.group(1)}"
                                # Look for position after "with"
                                position_part = cmd.lower().split("with")[1].strip()
                                valid_positions = {"GK", "DR", "DCR", "DCL", "DL", "MCR", "MC", "MCL", "AMR", "AML", "STC"}
                                
                                # Try to find the position
                                position = None
                                for pos in valid_positions:
                                    if pos in position_part.upper():
                                        position = pos
                                        break
                                
                                if position:
                                    print(f"Found substitution: {substitute_number} for {position}")
                                    make_substitution(substitute_number, position)
                                else:
                                    print(f"Could not find valid position in: {position_part}")

                    time.sleep(0.5)  # Wait between commands

            time.sleep(0.5)  

        else:
            # Only close menu if it was opened for instructions and we're done
            if instructions_applied > 0 and menu_open:
                if last_instruction in ["be more expressive", "be more disciplined"]:
                    time.sleep(0.2)
                close_instructions_menu_after_commands()
                menu_open = False
                instructions_applied = 0  
                last_instruction = None
            time.sleep(0.1)  

if __name__ == "__main__":
    main()