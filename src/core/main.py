import time
import keyboard
from speech_recognition import listen_for_command
from game_controls import pause_game, resume_game
from instructions import (
    open_instructions_menu, apply_instruction,
    close_instructions_menu, click_cancel_button,
    process_instruction_command
)
from substitutions import (
    make_substitution, open_substitution_menu,
    process_substitution_command, confirm_substitution
)
from mentalities import change_mentality_to
from shouts import trigger_shout
from ocr import read_positions_and_roles, save_positions_to_file
from config import (
    MENTALITIES, SHOUTS, INSTRUCTIONS, IN_TRANSITION_INSTRUCTIONS
)
import pyautogui
import os
import re

# Import in_transition after other imports to avoid circular dependency
from in_transition import navigate_to_in_transition, apply_in_transition_instruction

def split_commands(command):
    """Split a command into individual commands based on keywords."""
    print(f"\nDEBUG: Starting split_commands for: {command}")
    commands = []
    words = command.split()
    print(f"DEBUG: Split words: {words}")
    
    command_starters = {
        "mentality": ["very defensive", "very attacking", "attacking", "balanced", 
                     "defensive", "positive", "cautious"],
        "shout": ["encourage", "calm down", "focus", "fire up", "no pressure", 
                 "demand more", "praise", "berate"],
        "instruction": ["hit early crosses", "pass into space", "passing to space", 
                       "pass to space", "shoot on sight", "work ball into box", 
                       "work the ball into box", "be more expressive", 
                       "be more disciplined", "play for set pieces"],
        "in_transition": ["counter press", "regroup", "counter", "hold shape"],
        "substitution": ["swap", "change", "substitute", "bring on"]
    }
    
    i = 0
    while i < len(words):
        found_command = False
        current_word = words[i].lower()
        
        # Special handling for mentality commands
        if current_word in ["very", "attacking", "defensive", "balanced", "positive", "cautious"]:
            # Check if this is a mentality command
            if i + 1 < len(words):
                next_word = words[i + 1].lower()
                if next_word == "mentality" or next_word == "to":
                    # This is a mentality command
                    target_mentality = current_word
                    if current_word == "very":
                        # Look for the next word to complete "very defensive" or "very attacking"
                        if i + 2 < len(words):
                            target_mentality = f"very {words[i + 2].lower()}"
                            i += 3
                        else:
                            i += 2
                    else:
                        i += 2
                    
                    commands.append(("mentality", f"mentality to {target_mentality}"))
                    found_command = True
        
        # Check for other command types
        if not found_command:
            for cmd_type, starters in command_starters.items():
                for starter in starters:
                    if current_word == starter.split()[0]:
                        # For substitution commands, include the entire command
                        if cmd_type == "substitution":
                            # Get the rest of the words for the substitution command
                            remaining_words = words[i:]
                            full_command = ' '.join(remaining_words)
                            commands.append((cmd_type, full_command))
                            i = len(words)  # Move to end since we've used all remaining words
                            found_command = True
                            break
                        else:
                            # Try to match the full command for other types
                            potential_command = ' '.join(words[i:i+len(starter.split())])
                            if potential_command.lower() == starter:
                                commands.append((cmd_type, potential_command))
                                i += len(starter.split())
                                found_command = True
                                break
                if found_command:
                    break
        
        # If no command found, move to next word
        if not found_command:
            i += 1
    
    # Sort commands by priority (mentality -> shout -> instruction -> in_transition -> substitution)
    command_priority = {
        "mentality": 1,
        "shout": 2,
        "instruction": 3,
        "in_transition": 4,
        "substitution": 5
    }
    sorted_commands = sorted(commands, key=lambda x: command_priority[x[0]])
    print(f"\nDEBUG: Final sorted commands: {sorted_commands}")
    return sorted_commands

def process_commands(text):
    """Process voice commands and execute them in the game."""
    print("\nProcessing commands...")
    
    # Clean up the command text
    text = text.lower().strip()
    
    # Handle common speech recognition errors
    text = text.replace("st ", "standard ")
    text = text.replace("ard ", "standard ")
    
    # Split text into individual commands if there are multiple
    # First split by commas, then by 'and'
    commands = []
    for part in text.split(','):
        commands.extend([cmd.strip() for cmd in part.split('and')])
    commands = [cmd for cmd in commands if cmd]  # Remove empty commands
    print(f"DEBUG: Split commands: {commands}")
    
    # Track menu states
    instructions_menu_open = False
    in_transition = False
    substitutions_menu_open = False
    
    # Group commands by type for efficient processing
    command_groups = {
        "mentality": [],
        "shout": [],
        "instruction": [],
        "in_transition": [],
        "substitution": []
    }
    
    # First, categorize all commands
    for command in commands:
        actions = split_commands(command)
        for action_type, action_command in actions:
            command_groups[action_type].append(action_command)
    
    # Process commands in priority order
    # 1. Mentalities (no menu needed)
    for command in command_groups["mentality"]:
        print(f"\nDEBUG: Processing mentality command: {command}")
        if change_mentality_to(command):
            print(f"Successfully processed mentality command: {command}")
        else:
            print(f"Failed to process mentality command: {command}")
        time.sleep(0.5)
    
    # 2. Shouts (no menu needed)
    for command in command_groups["shout"]:
        print(f"\nDEBUG: Processing shout command: {command}")
        if trigger_shout(command):
            print(f"Successfully processed shout command: {command}")
        else:
            print(f"Failed to process shout command: {command}")
        time.sleep(0.5)
    
    # 3. Instructions and In Transition (both need instructions menu)
    if command_groups["instruction"] or command_groups["in_transition"]:
        # Open instructions menu only once
        if not instructions_menu_open:
            print("Opening instructions menu...")
            if open_instructions_menu():
                instructions_menu_open = True
                time.sleep(0.5)
            else:
                print("Failed to open instructions menu")
                return
        
        # Process all instruction commands
        for command in command_groups["instruction"]:
            print(f"\nDEBUG: Processing instruction command: {command}")
            if apply_instruction(command):
                print(f"Successfully processed instruction command: {command}")
            else:
                print(f"Failed to process instruction command: {command}")
            time.sleep(0.5)
        
        # Process all In Transition commands
        for command in command_groups["in_transition"]:
            print(f"\nDEBUG: Processing In Transition command: {command}")
            if not in_transition:
                if navigate_to_in_transition(True):  # Pass True since menu is already open
                    in_transition = True
                    time.sleep(0.5)
                else:
                    print("Failed to navigate to In Transition menu")
                    continue
            
            if apply_in_transition_instruction(command):
                print(f"Successfully processed In Transition command: {command}")
            else:
                print(f"Failed to process In Transition command: {command}")
            time.sleep(0.5)
        
        # Close instructions menu after processing all instruction-related commands
        if instructions_menu_open:
            close_instructions_menu()
            instructions_menu_open = False
        if in_transition:
            click_cancel_button()
            in_transition = False
    
    # 4. Substitutions (need substitutions menu)
    if command_groups["substitution"]:
        # Open substitutions menu
        print("Opening substitutions menu...")
        if open_substitution_menu():
            substitutions_menu_open = True
            time.sleep(0.5)
        else:
            print("Failed to open substitutions menu")
            return
        
        # Process all substitution commands
        for command in command_groups["substitution"]:
            print(f"\nDEBUG: Processing substitution command: {command}")
            if process_substitution_command(command):
                print(f"Successfully processed substitution command: {command}")
            else:
                print(f"Failed to process substitution command: {command}")
            time.sleep(0.5)
        
        # Close substitutions menu
        if substitutions_menu_open:
            confirm_substitution()
            substitutions_menu_open = False

def process_text_command():
    """Get and process a text command from the user."""
    print("\nEnter your command (or 'exit' to quit):")
    command = input().strip()
    
    if command.lower() == 'exit':
        return False
    
    if command:
        print(f"Processing text command: {command}")
        process_commands(command)
    
    return True

def main():
    print("Hold Caps Lock to activate voice commands.")
    print("Press 'T' to enter text command mode.")
    print("Press 'P' to read positions and roles.")
    print("Press 'Space' to pause/resume the game.")
    print("Press 'Q' to quit the program.")
    
    menu_open = False
    instructions_applied = 0
    p_key_pressed = False
    space_key_pressed = False
    t_key_pressed = False
    last_instruction = None

    while True:
        # Check for quit command
        if keyboard.is_pressed('q'):
            print("Quitting program...")
            break

        # Check for text command mode
        if keyboard.is_pressed('t') and not t_key_pressed:
            t_key_pressed = True
            print("\nEntering text command mode...")
            while process_text_command():
                pass
            print("Exiting text command mode...")
            time.sleep(0.5)
        elif not keyboard.is_pressed('t'):
            t_key_pressed = False

        # Check for position reading command
        if keyboard.is_pressed('p') and not p_key_pressed:
            p_key_pressed = True
            print("Reading positions and roles...")
            positions_data = read_positions_and_roles()
            if positions_data:
                save_positions_to_file(positions_data)
            time.sleep(0.5)
        elif not keyboard.is_pressed('p'):
            p_key_pressed = False

        # Check for pause/resume command
        if keyboard.is_pressed('space') and not space_key_pressed:
            space_key_pressed = True
            if not resume_game():
                pause_game()
            time.sleep(0.5)
        elif not keyboard.is_pressed('space'):
            space_key_pressed = False

        # Voice command system
        if keyboard.is_pressed('caps lock'):
            print("\nSpeak your command...")
            command = listen_for_command()

            if command:
                print(f"Command: {command}")
                
                # Clean up the command string
                command = command.replace(',', ' ').replace('.', ' ')
                command = ' '.join(command.split())
                
                # Process commands
                process_commands(command)

            time.sleep(0.5)
        else:
            time.sleep(0.1)

if __name__ == "__main__":
    main() 