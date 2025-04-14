import pytesseract
from PIL import Image
import re

# Set the path to the tesseract executable (if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image_path = r'C:\Users\Pedro Barbosa\Desktop\testeteste.jpg'
image = Image.open(image_path)
image_width, image_height = image.size

start_x, start_y = 700, 183  
width, height = 130, 1  
height = image_height - start_y 

roi = (start_x, start_y, start_x + width, start_y + height)

cropped_image = image.crop(roi)

# Resize the image to triple its size (for better accuracy)
new_width = cropped_image.width * 3
new_height = cropped_image.height * 3
cropped_image = cropped_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Convert image to grayscale for better OCR
cropped_image = cropped_image.convert('L')

# OCR with PSM 11 for sparse text
ocr_output = pytesseract.image_to_string(cropped_image, config='--oem 3 --psm 11', lang='eng')

# Replace "$" with "S"
ocr_output = ocr_output.replace('$', 'S')

# Specific roles to keep
valid_roles = {"GK", "DR", "DCR", "DCL", "DL", "MCR", "MC", "MCL", "AMR", "AML", "STC"}

# Split OCR output into words and filter out those that are not in the valid roles
filtered_words = []
s_items = []

# Counter for valid roles
valid_role_count = 0

for word in ocr_output.split():
    word_upper = word.upper()
    
    # Check for valid roles first
    if word_upper in valid_roles:
        filtered_words.append(word_upper)
        valid_role_count += 1
    elif valid_role_count >= 11:
        # After 11 valid roles, start looking for S1 to S12
        s_items_pattern = r'\bS[1-9]|S1[0-2]\b'  # Matches S1 to S12
        if re.match(s_items_pattern, word_upper):
            s_items.append(word_upper)

# Reconstruct the output after filtering unwanted words and finding S items
filtered_output = " ".join(filtered_words)
s_items_output = " ".join(s_items)

print("Filtered OCR Output (Valid Roles):")
print(filtered_output)

print("\nS Items (S1 to S12):")
print(s_items_output)

# Optionally, save the output to a file
with open('position_role_output.txt', 'w') as file:
    file.write(f"Filtered Roles: {filtered_output}\n")
    file.write(f"S Items: {s_items_output}\n")

print("OCR process completed. Check 'position_role_output.txt' for results.")
