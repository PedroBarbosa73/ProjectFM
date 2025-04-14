import time
import keyboard
from speech_recognition import listen_for_command
from game_controls import pause_game, resume_game
from instructions import (
    open_instructions_menu, apply_instruction,
    close_instructions_menu, click_cancel_button,
    process_instruction_command
)
from substitutions import make_substitution, open_substitution_menu
from mentalities import change_mentality_to
from shouts import trigger_shout
from ocr import read_positions_and_roles, save_positions_to_file
from config import (
    MENTALITIES, SHOUTS, INSTRUCTIONS, ENGAGEMENT_POSITIONS,
    DEFENSIVE_LINE_POSITIONS, POSITION_MAPPINGS
)
import pyautogui
import os
import re

# Import out_of_possession after other imports to avoid circular dependency
from out_of_possession import navigate_to_out_of_possession, adjust_engagement_line, adjust_defensive_line

def split_commands(command):
    """Split a command into individual commands based on keywords."""
    print(f"Splitting command: {command}")
    
    # Split by commas only
    command_parts = [part.strip() for part in command.split(',')]
    command_parts = [p for p in command_parts if p]  # Remove empty parts
    print(f"Split by commas: {command_parts}")
    
    # Define command categories and their keywords with priorities
    command_categories = {
        "mentality": (1, MENTALITIES),
        "shout": (2, SHOUTS),
        "instruction": (3, INSTRUCTIONS + [
            # High press variations
            "high press", "press high", "high block", "high pressure", "high pressing",
            # Mid block variations
            "mid block", "middle block", "medium block", "mid pressure", "medium pressure",
            # Low block variations
            "low block", "drop deep", "low engagement", "low pressure", "low pressing",
            # Defensive line variations
            "much higher defensive line", "much higher defense", "much higher defence",
            "much higher back line", "much higher backline", "much higher line",
            "higher defensive line", "higher defense", "higher defence",
            "higher back line", "higher backline", "higher line",
            "standard defensive line", "normal defensive line", "standard defense",
            "standard defence", "normal defense", "normal defence",
            "standard back line", "normal back line", "standard backline",
            "lower defensive line", "lower defense", "lower defence",
            "lower back line", "lower backline", "lower line",
            "much lower defensive line", "much lower defense", "much lower defence",
            "much lower back line", "much lower backline", "much lower line"
        ]),
        "substitution": (4, ["swap", "change", "substitute"])
    }
    
    commands = []
    for part in command_parts:
        # Try to match the entire part first
        found_command = False
        for category, (priority, keywords) in command_categories.items():
            for keyword in keywords:
                if part.lower().startswith(keyword.lower()):
                    commands.append((priority, category, part))
                    found_command = True
                    break
            if found_command:
                break
        
        # If no full match found, try to find partial matches
        if not found_command:
            i = 0
            while i < len(part):
                found_category = False
                for category, (priority, keywords) in command_categories.items():
                    for keyword in keywords:
                        if part[i:].lower().startswith(keyword.lower()):
                            # Found a command, extract it
                            end_index = part.find(".", i)
                            if end_index == -1:
                                end_index = len(part)
                            current_command = part[i:end_index].strip()
                            commands.append((priority, category, current_command))
                            i = end_index + 1
                            found_category = True
                            break
                    if found_category:
                        break
                if not found_category:
                    i += 1
    
    # Sort commands by priority
    commands.sort(key=lambda x: x[0])
    # Remove priority from output
    commands = [(category, cmd) for _, category, cmd in commands]
    
    print(f"Split into commands (sorted by priority): {commands}")
    return commands

def process_command(command):
    """Process a single command."""
    print(f"Processing command: {command}")
    
    # Determine command type and process accordingly
    command_lower = command.lower()
    
    # 1. Mentalities (highest priority)
    if command in MENTALITIES:
        return change_mentality_to(command)
    
    # 2. Shouts
    elif command in SHOUTS:
        return trigger_shout(command)
    
    # 3. Instructions
    elif command in INSTRUCTIONS:
        print(f"Processing instruction: {command}")
        return process_instruction_command(command)
    
    # 4. Defensive Shapes (Out of Possession)
    elif any(keyword in command_lower for keyword in [
        "press", "block", "defensive line", "defense", "defence",
        "high press", "mid block", "low block", "high pressure", "mid pressure", "low pressure",
        "drop deep", "low engagement", "high pressure", "high pressing", "mid pressure", "mid pressing",
        "low pressure", "low pressing", "much higher defensive line", "higher defensive line",
        "standard defensive line", "lower defensive line", "much lower defensive line"
    ]):
        print(f"Processing defensive shape: {command}")
        # First open instructions menu
        if not open_instructions_menu():
            print("Failed to open instructions menu")
            return False
        time.sleep(0.5)
        
        # Navigate to out of possession
        if not navigate_to_out_of_possession(True):
            print("Failed to navigate to out of possession")
            return False
        time.sleep(0.5)
        
        # Adjust engagement line based on command
        if "low block" in command_lower:
            return adjust_engagement_line("low block")
        elif "mid block" in command_lower:
            return adjust_engagement_line("mid block")
        elif "high press" in command_lower:
            return adjust_engagement_line("high press")
        else:
            print(f"Unrecognized defensive shape command: {command}")
            return False
    
    # 5. Substitutions (lowest priority)
    elif any(keyword in command_lower for keyword in ["swap", "change", "substitute"]):
        print(f"\nDEBUG: Processing substitution command: {command}")
        # Extract substitute number and position
        substitute_match = re.search(r'S?(\d{1,2})', command.upper())
        if not substitute_match:
            print("Could not find substitute number in command")
            return False
            
        substitute_number = f"S{substitute_match.group(1)}"
        print(f"Found substitute number: {substitute_number}")
        
        # First open the substitutions menu
        print("Opening substitutions menu...")
        if not open_substitution_menu():
            print("Failed to open substitutions menu")
            return False
            
        # Wait for menu to fully open
        time.sleep(1.5)
        
        # Extract position
        print(f"\nDEBUG: Looking for position in command: {command_lower}")
        print(f"DEBUG: Available position mappings: {POSITION_MAPPINGS}")
        position = None
        for natural_name, code in POSITION_MAPPINGS.items():
            print(f"DEBUG: Checking if '{natural_name}' is in command")
            if natural_name in command_lower:
                position = code
                print(f"DEBUG: Found position match! '{natural_name}' -> '{code}'")
                break
                
        if not position:
            print("Could not find valid position in command")
            print(f"DEBUG: Command was: {command_lower}")
            return False
            
        print(f"Found position: {position}")
        return make_substitution(substitute_number, position)
    
    else:
        print(f"Command not recognized: {command}")
        return False

def get_text_command():
    """Get a command from text input."""
    print("\nEnter your command (or 'exit' to quit):")
    command = input().strip()
    return command

def main():
    print("Hold Caps Lock to activate voice commands.")
    print("Press 'T' to enter text command mode.")
    print("Press 'P' to read positions and roles.")
    print("Press 'Space' to pause/resume the game.")
    print("Press 'Q' to quit the program.")
    
    while True:
        try:
            # Check for quit command
            if keyboard.is_pressed('q'):
                print("Quitting program...")
                break

            # Check for text command mode
            if keyboard.is_pressed('t'):
                print("\nEntering text command mode...")
                while True:
                    command = get_text_command()
                    if command.lower() == 'exit':
                        print("Exiting text command mode...")
                        break
                    
                    if command:
                        print(f"Processing text command: {command}")
                        commands = split_commands(command)
                        for category, cmd in commands:
                            print(f"Processing {category} command: {cmd}")
                            process_command(cmd)
                            time.sleep(0.5)
                time.sleep(0.5)  # Prevent multiple activations
            
            # Check for position reading
            if keyboard.is_pressed('p'):
                print("Reading positions and roles...")
                positions = read_positions_and_roles()
                if positions:
                    save_positions_to_file(positions)
                time.sleep(0.5)  # Prevent multiple readings
            
            # Check for pause/resume
            if keyboard.is_pressed('space'):
                print("Toggling game pause...")
                if pyautogui.locateOnScreen("pause.png", confidence=0.9):
                    pause_game()
                else:
                    resume_game()
                time.sleep(0.5)  # Prevent multiple toggles
            
            # Check for voice command
            if keyboard.is_pressed('caps lock'):
                print("Listening for voice command...")
                command = listen_for_command()
                if command:
                    print(f"Voice command received: {command}")
                    commands = split_commands(command)
                    for category, cmd in commands:
                        print(f"Processing {category} command: {cmd}")
                        process_command(cmd)
                        time.sleep(0.5)
                time.sleep(0.5)  # Prevent multiple activations
            
            time.sleep(0.1)  # Reduce CPU usage
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            time.sleep(1)  # Wait before retrying

if __name__ == "__main__":
    main() 