import time
import keyboard
from speech_recognition import listen_for_command
from game_controls import pause_game, resume_game
from instructions import (
    open_instructions_menu, apply_instruction,
    close_instructions_menu, click_cancel_button,
    process_instruction_command, is_instructions_menu_open
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
        "instruction": (3, INSTRUCTIONS),  # Regular instructions only
        "defensive_shape": (4, [  # Defensive shapes with higher priority than regular instructions
            # High press variations
            "high press", "press high", "high block", "high pressure", "high pressing",
            # Mid block variations
            "mid block", "middle block", "medium block", "mid pressure", "medium pressure",
            # Low block variations
            "low block", "drop deep", "low engagement", "low pressure", "low pressing",
            # Defensive line variations
            "defensive line", "defense", "defence", "back line", "backline", "line",
            "much higher", "higher", "standard", "normal", "lower", "much lower"
        ]),
        "substitution": (5, ["swap", "change", "substitute"])
    }
    
    # Process each command part
    commands = []
    for part in command_parts:
        part_lower = part.lower()
        categorized = False
        
        # Check each category
        for category, (priority, keywords) in command_categories.items():
            if any(keyword in part_lower for keyword in keywords):
                commands.append((category, part))
                categorized = True
                break
        
        if not categorized:
            print(f"Warning: Could not categorize command: {part}")
    
    # Sort commands by priority (mentality -> shout -> instruction -> defensive_shape -> substitution)
    command_priority = {
        "mentality": 1,
        "shout": 2,
        "instruction": 3,
        "defensive_shape": 4,
        "substitution": 5
    }
    sorted_commands = sorted(commands, key=lambda x: command_priority[x[0]])
    print(f"\nDEBUG: Final sorted commands: {sorted_commands}")
    return sorted_commands

def process_command(command, keep_menu_open=False):
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
    
    # 3. Regular Instructions
    elif command in INSTRUCTIONS:
        print(f"Processing regular instruction: {command}")
        return process_instruction_command(command, close_menu=not keep_menu_open)
    
    # 4. Defensive Shapes (Out of Possession)
    elif any(keyword in command_lower for keyword in [
        "press", "block", "defensive line", "defense", "defence",
        "high press", "mid block", "low block", "high pressure", "mid pressure", "low pressure",
        "drop deep", "low engagement", "high pressure", "high pressing", "mid pressure", "mid pressing",
        "low pressure", "low pressing", "much higher defensive line", "higher defensive line",
        "standard defensive line", "lower defensive line", "much lower defensive line"
    ]):
        print(f"Processing defensive shape: {command}")
        
        # Check if instructions menu is already open
        try:
            if not is_instructions_menu_open():
                # Only open menu if it's not already open
                if not open_instructions_menu():
                    print("Failed to open instructions menu")
                    return False
                time.sleep(0.5)
        except Exception as e:
            print(f"Error checking instructions menu state: {e}")
            # If we can't check the state, try to open the menu
            if not open_instructions_menu():
                print("Failed to open instructions menu")
                return False
            time.sleep(0.5)
        
        # Navigate to out of possession
        if not navigate_to_out_of_possession(True):
            print("Failed to navigate to out of possession")
            return False
        time.sleep(0.5)
        
        # Check for defensive line command first
        if any(keyword in command_lower for keyword in [
            "defensive line", "defense", "defence", "back line", "backline", "line"
        ]):
            print(f"Adjusting defensive line based on command: {command}")
            # Determine the target position
            if "much higher" in command_lower:
                return adjust_defensive_line("much higher")
            elif "higher" in command_lower:
                return adjust_defensive_line("higher")
            elif "standard" in command_lower or "normal" in command_lower:
                return adjust_defensive_line("standard")
            elif "lower" in command_lower:
                return adjust_defensive_line("lower")
            elif "much lower" in command_lower:
                return adjust_defensive_line("much lower")
            else:
                print(f"Unrecognized defensive line command: {command}")
                return False
        
        # Then check for engagement line command
        elif any(keyword in command_lower for keyword in [
            "press", "block", "high press", "mid block", "low block",
            "high pressure", "mid pressure", "low pressure",
            "drop deep", "low engagement", "high pressure", "high pressing",
            "mid pressure", "mid pressing", "low pressure", "low pressing"
        ]):
            print(f"Adjusting engagement line based on command: {command}")
            if "low block" in command_lower:
                return adjust_engagement_line("low block")
            elif "mid block" in command_lower:
                return adjust_engagement_line("mid block")
            elif "high press" in command_lower:
                return adjust_engagement_line("high press")
            else:
                print(f"Unrecognized engagement line command: {command}")
                return False
        else:
            print(f"Unrecognized defensive shape command: {command}")
            return False
    
    # 5. Substitutions
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
                        for i, (category, cmd) in enumerate(commands):
                            print(f"Processing {category} command: {cmd}")
                            # Keep menu open if there are defensive shapes coming
                            keep_menu_open = any(cat == "defensive_shape" for cat, _ in commands[i+1:])
                            process_command(cmd, keep_menu_open=keep_menu_open)
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
                print("Speak your command...")
                command = listen_for_command()
                if command:
                    print(f"Received command: {command}")
                    
                    # Split command into individual commands
                    commands = split_commands(command)
                    
                    # Process each command
                    for i, (category, cmd) in enumerate(commands):
                        print(f"Processing {category} command: {cmd}")
                        # Keep menu open if there are defensive shapes coming
                        keep_menu_open = any(cat == "defensive_shape" for cat, _ in commands[i+1:])
                        process_command(cmd, keep_menu_open=keep_menu_open)
                        time.sleep(0.5)  # Wait between commands
                
                time.sleep(0.5)  # Prevent multiple activations
            
            time.sleep(0.1)  # Reduce CPU usage
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(1)  # Wait before retrying

if __name__ == "__main__":
    main() 