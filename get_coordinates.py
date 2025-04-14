import pyautogui
import time
import keyboard
import json
import os

def get_coordinates():
    """Get coordinates by hovering over elements and pressing 'c' to capture."""
    print("\n=== Coordinate Capture Tool ===")
    print("Instructions:")
    print("1. Hover your mouse over the element you want to capture")
    print("2. Press 'c' to capture the coordinates")
    print("3. Press 'q' to quit")
    print("4. Press 's' to save current coordinates")
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    coordinates = {
        # Main Menu Buttons
        "INSTRUCTIONS_MENU_COORDS": {"x": 0, "y": 0, "width": 0, "height": 0},
        "MENTALITY_MENU_COORDS": {"x": 0, "y": 0, "width": 0, "height": 0},
        "SHOUT_MENU_COORDS": {"x": 0, "y": 0, "width": 0, "height": 0},
        "SUBSTITUTION_MENU_COORDS": {"x": 0, "y": 0, "width": 0, "height": 0},
        
        # Instructions Menu Buttons
        "OUT_OF_POSSESSION_MENU_COORDS": {"x": 0, "y": 0, "width": 0, "height": 0},
        "IN_POSSESSION_MENU_COORDS": {"x": 0, "y": 0, "width": 0, "height": 0},
        
        # Defensive Line Markers
        "DEFENSIVE_LINE_COORDS": {
            "much higher": {"x": 0, "y": 0},
            "higher": {"x": 0, "y": 0},
            "standard": {"x": 0, "y": 0},
            "lower": {"x": 0, "y": 0},
            "much lower": {"x": 0, "y": 0}
        },
        
        # Line of Engagement Markers
        "ENGAGEMENT_LINE_COORDS": {
            "high": {"x": 0, "y": 0},
            "mid": {"x": 0, "y": 0},
            "low": {"x": 0, "y": 0}
        },
        
        # Action Buttons
        "OK_BUTTON_COORDS": {"x": 0, "y": 0, "width": 0, "height": 0},
        "CANCEL_BUTTON_COORDS": {"x": 0, "y": 0, "width": 0, "height": 0},
        "CONFIRM_SUB_BUTTON_COORDS": {"x": 0, "y": 0, "width": 0, "height": 0},
        
        # Mentality Buttons
        "MENTALITY_BUTTON_COORDS": {
            "very defensive": {"x": 0, "y": 0},
            "defensive": {"x": 0, "y": 0},
            "balanced": {"x": 0, "y": 0},
            "attacking": {"x": 0, "y": 0},
            "very attacking": {"x": 0, "y": 0}
        },
        
        # Shout Buttons
        "SHOUT_BUTTON_COORDS": {
            "get stuck in": {"x": 0, "y": 0},
            "stay on feet": {"x": 0, "y": 0},
            "get further forward": {"x": 0, "y": 0},
            "hold shape": {"x": 0, "y": 0},
            "push higher up": {"x": 0, "y": 0},
            "drop deeper": {"x": 0, "y": 0},
            "press more urgently": {"x": 0, "y": 0},
            "be more expressive": {"x": 0, "y": 0},
            "show some passion": {"x": 0, "y": 0},
            "calm down": {"x": 0, "y": 0},
            "concentrate": {"x": 0, "y": 0},
            "demand more": {"x": 0, "y": 0},
            "encourage": {"x": 0, "y": 0},
            "no pressure": {"x": 0, "y": 0},
            "tighter marking": {"x": 0, "y": 0},
            "zonal marking": {"x": 0, "y": 0},
            "man marking": {"x": 0, "y": 0},
            "close down more": {"x": 0, "y": 0},
            "stand off more": {"x": 0, "y": 0},
            "get creative": {"x": 0, "y": 0},
            "be more disciplined": {"x": 0, "y": 0},
            "roam from position": {"x": 0, "y": 0},
            "stick to position": {"x": 0, "y": 0},
            "run at defence": {"x": 0, "y": 0},
            "pass shorter": {"x": 0, "y": 0},
            "pass into space": {"x": 0, "y": 0},
            "pump ball into box": {"x": 0, "y": 0},
            "clear ball to flanks": {"x": 0, "y": 0},
            "retain possession": {"x": 0, "y": 0},
            "get ball forward": {"x": 0, "y": 0},
            "shoot on sight": {"x": 0, "y": 0},
            "work ball into box": {"x": 0, "y": 0},
            "cross more often": {"x": 0, "y": 0},
            "cross less often": {"x": 0, "y": 0},
            "play wider": {"x": 0, "y": 0},
            "play narrower": {"x": 0, "y": 0},
            "higher tempo": {"x": 0, "y": 0},
            "lower tempo": {"x": 0, "y": 0},
            "waste time": {"x": 0, "y": 0},
            "quick throw-ins": {"x": 0, "y": 0},
            "take a breather": {"x": 0, "y": 0}
        },
        
        # Substitution Buttons
        "SUBSTITUTION_BUTTON_COORDS": {
            "substitute": {"x": 0, "y": 0},
            "confirm": {"x": 0, "y": 0}
        }
    }
    
    current_element = None
    current_sub_element = None
    
    while True:
        if keyboard.is_pressed('q'):
            print("\nQuitting...")
            break
        elif keyboard.is_pressed('c'):
            x, y = pyautogui.position()
            print(f"\nCaptured coordinates: ({x}, {y})")
            
            if current_element and current_sub_element:
                if current_element in ["DEFENSIVE_LINE_COORDS", "ENGAGEMENT_LINE_COORDS", 
                                     "MENTALITY_BUTTON_COORDS", "SHOUT_BUTTON_COORDS", 
                                     "SUBSTITUTION_BUTTON_COORDS"]:
                    coordinates[current_element][current_sub_element]["x"] = x
                    coordinates[current_element][current_sub_element]["y"] = y
                    print(f"Saved coordinates for {current_element} -> {current_sub_element}")
                else:
                    coordinates[current_element]["x"] = x
                    coordinates[current_element]["y"] = y
                    print(f"Saved coordinates for {current_element}")
            
            time.sleep(0.5)  # Prevent multiple captures
        elif keyboard.is_pressed('s'):
            save_coordinates(coordinates)
            print("\nCoordinates saved to coordinates.py")
            time.sleep(0.5)
        elif keyboard.is_pressed('1'):
            current_element = "INSTRUCTIONS_MENU_COORDS"
            current_sub_element = None
            print(f"\nSelected: {current_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('2'):
            current_element = "MENTALITY_MENU_COORDS"
            current_sub_element = None
            print(f"\nSelected: {current_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('3'):
            current_element = "SHOUT_MENU_COORDS"
            current_sub_element = None
            print(f"\nSelected: {current_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('4'):
            current_element = "SUBSTITUTION_MENU_COORDS"
            current_sub_element = None
            print(f"\nSelected: {current_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('5'):
            current_element = "OUT_OF_POSSESSION_MENU_COORDS"
            current_sub_element = None
            print(f"\nSelected: {current_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('6'):
            current_element = "IN_POSSESSION_MENU_COORDS"
            current_sub_element = None
            print(f"\nSelected: {current_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('7'):
            current_element = "DEFENSIVE_LINE_COORDS"
            print("\nSelect Defensive Line position:")
            print("f: much higher")
            print("g: higher")
            print("h: standard")
            print("j: lower")
            print("k: much lower")
            time.sleep(0.5)
        elif keyboard.is_pressed('8'):
            current_element = "ENGAGEMENT_LINE_COORDS"
            print("\nSelect Engagement Line position:")
            print("z: high")
            print("x: mid")
            print("c: low")
            time.sleep(0.5)
        elif keyboard.is_pressed('9'):
            current_element = "OK_BUTTON_COORDS"
            current_sub_element = None
            print(f"\nSelected: {current_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('0'):
            current_element = "CANCEL_BUTTON_COORDS"
            current_sub_element = None
            print(f"\nSelected: {current_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('m'):
            current_element = "MENTALITY_BUTTON_COORDS"
            print("\nSelect Mentality:")
            print("1: very defensive")
            print("2: defensive")
            print("3: balanced")
            print("4: attacking")
            print("5: very attacking")
            time.sleep(0.5)
        elif keyboard.is_pressed('s'):
            current_element = "SHOUT_BUTTON_COORDS"
            print("\nSelect Shout (use number keys 1-9 for first digit, then a-z for second digit)")
            time.sleep(0.5)
        elif keyboard.is_pressed('u'):
            current_element = "SUBSTITUTION_BUTTON_COORDS"
            print("\nSelect Substitution Button:")
            print("1: substitute")
            print("2: confirm")
            time.sleep(0.5)
        
        # Handle sub-elements for different menus
        elif keyboard.is_pressed('f'):
            if current_element == "DEFENSIVE_LINE_COORDS":
                current_sub_element = "much higher"
                print(f"\nSelected: {current_element} -> {current_sub_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('g'):
            if current_element == "DEFENSIVE_LINE_COORDS":
                current_sub_element = "higher"
                print(f"\nSelected: {current_element} -> {current_sub_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('h'):
            if current_element == "DEFENSIVE_LINE_COORDS":
                current_sub_element = "standard"
                print(f"\nSelected: {current_element} -> {current_sub_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('j'):
            if current_element == "DEFENSIVE_LINE_COORDS":
                current_sub_element = "lower"
                print(f"\nSelected: {current_element} -> {current_sub_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('k'):
            if current_element == "DEFENSIVE_LINE_COORDS":
                current_sub_element = "much lower"
                print(f"\nSelected: {current_element} -> {current_sub_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('z'):
            if current_element == "ENGAGEMENT_LINE_COORDS":
                current_sub_element = "high"
                print(f"\nSelected: {current_element} -> {current_sub_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('x'):
            if current_element == "ENGAGEMENT_LINE_COORDS":
                current_sub_element = "mid"
                print(f"\nSelected: {current_element} -> {current_sub_element}")
            time.sleep(0.5)
        elif keyboard.is_pressed('c'):
            if current_element == "ENGAGEMENT_LINE_COORDS":
                current_sub_element = "low"
                print(f"\nSelected: {current_element} -> {current_sub_element}")
            time.sleep(0.5)
        
        time.sleep(0.1)  # Prevent high CPU usage

def save_coordinates(coordinates):
    """Save coordinates to coordinates.py file."""
    with open('coordinates.py', 'w') as f:
        f.write('"""\nCoordinates for all buttons and markers in the game.\nThese are the default positions, but we\'ll still have image recognition as a fallback.\n"""\n\n')
        
        for key, value in coordinates.items():
            f.write(f"# {key.replace('_', ' ').title()}\n")
            f.write(f"{key} = {json.dumps(value, indent=4)}\n\n")

if __name__ == "__main__":
    print("\n=== Coordinate Capture Tool ===")
    print("Controls:")
    print("1: Instructions Menu")
    print("2: Mentality Menu")
    print("3: Shout Menu")
    print("4: Substitution Menu")
    print("5: Out of Possession Menu")
    print("6: In Possession Menu")
    print("7: Defensive Line Markers")
    print("8: Engagement Line Markers")
    print("9: OK Button")
    print("0: Cancel Button")
    print("m: Mentality Buttons")
    print("s: Shout Buttons")
    print("u: Substitution Buttons")
    print("\nFor Defensive Line Markers (after pressing 7):")
    print("f: much higher")
    print("g: higher")
    print("h: standard")
    print("j: lower")
    print("k: much lower")
    print("\nFor Engagement Line Markers (after pressing 8):")
    print("z: high")
    print("x: mid")
    print("c: low")
    print("\nFor Mentality Buttons (after pressing m):")
    print("1: very defensive")
    print("2: defensive")
    print("3: balanced")
    print("4: attacking")
    print("5: very attacking")
    print("\nFor Substitution Buttons (after pressing u):")
    print("1: substitute")
    print("2: confirm")
    print("\nc: Capture coordinates")
    print("s: Save coordinates")
    print("q: Quit")
    
    get_coordinates() 