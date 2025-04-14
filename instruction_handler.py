import time
from instructions import open_instructions_menu, apply_instruction, close_instructions_menu
from in_transition import navigate_to_in_transition, apply_in_transition_instruction
from out_of_possession import navigate_to_out_of_possession, apply_out_of_possession_instruction

def handle_instruction_command(command):
    """Handle instruction commands in the correct order: In Possession -> In Transition -> Out of Possession"""
    try:
        # First check if it's an In Possession instruction
        from config import INSTRUCTIONS
        if command in INSTRUCTIONS:
            print(f"Handling In Possession instruction: {command}")
            if not open_instructions_menu():
                print("Failed to open instructions menu")
                return False
            success = apply_instruction(command)
            close_instructions_menu()
            return success

        # Then check if it's an In Transition instruction
        from config import IN_TRANSITION_IMAGES
        if command in IN_TRANSITION_IMAGES:
            print(f"Handling In Transition instruction: {command}")
            if not navigate_to_in_transition():
                print("Failed to navigate to In Transition menu")
                return False
            success = apply_in_transition_instruction(command)
            close_instructions_menu()
            return success

        # Finally check if it's an Out of Possession instruction
        from config import OUT_OF_POSSESSION_IMAGES
        if command in OUT_OF_POSSESSION_IMAGES:
            print(f"Handling Out of Possession instruction: {command}")
            if not navigate_to_out_of_possession():
                print("Failed to navigate to Out of Possession menu")
                return False
            success = apply_out_of_possession_instruction(command)
            close_instructions_menu()
            return success

        print(f"Unknown instruction command: {command}")
        return False

    except Exception as e:
        print(f"Error handling instruction command: {e}")
        return False 