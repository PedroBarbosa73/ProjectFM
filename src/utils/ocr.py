import pyautogui
import pytesseract
from PIL import Image
import re
from config import TESSERACT_PATH

# Set the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

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