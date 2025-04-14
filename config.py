import os

# Azure Speech Services Configuration
AZURE_SPEECH_KEY = "5PkPNpEmedkaolUo07EJuH5iQR151yrcsk194DyqM28JMROhCQknJQQJ99BCACYeBjFXJ3w3AAAYACOG6u6s"
AZURE_REGION = "eastus"

# Tesseract Configuration
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Base image directory
BASE_IMAGE_DIR = r"C:\Users\Pedro Barbosa\Desktop\images"

# Instructions Menu Images
INSTRUCTIONS_MENU_IMAGE = os.path.join(BASE_IMAGE_DIR, "instructions", "instructions_menu.png")
OK_BUTTON_IMAGE = os.path.join(BASE_IMAGE_DIR, "instructions", "ok_button.png")
CANCEL_BUTTON_IMAGE = os.path.join(BASE_IMAGE_DIR, "cancel.png")
IN_POSSESSION_BUTTON_IMAGE = os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession_button.png")

# Out of Possession Menu
OUT_OF_POSSESSION_DIR = os.path.join(BASE_IMAGE_DIR, "instructions", "out_of_possession")
OUT_OF_POSSESSION_MENU = os.path.join(OUT_OF_POSSESSION_DIR, "out_of_possession_menu.png")

# In Transition
IN_TRANSITION_DIR = os.path.join(BASE_IMAGE_DIR, "instructions", "in_transition")
IN_TRANSITION_MENU = os.path.join(IN_TRANSITION_DIR, "in_transition_menu.png")

# In Transition Instructions
IN_TRANSITION_IMAGES = {
    "counter press": {
        "unselected": os.path.join(IN_TRANSITION_DIR, "counter_press_un.png"),
        "selected": os.path.join(IN_TRANSITION_DIR, "counter_press_sel.png"),
        "hover": os.path.join(IN_TRANSITION_DIR, "counter_press_hover.png")
    },
    "regroup": {
        "unselected": os.path.join(IN_TRANSITION_DIR, "regroup_un.png"),
        "selected": os.path.join(IN_TRANSITION_DIR, "regroup_sel.png"),
        "hover": os.path.join(IN_TRANSITION_DIR, "regroup_hover.png")
    },
    "counter": {
        "unselected": os.path.join(IN_TRANSITION_DIR, "counter_un.png"),
        "selected": os.path.join(IN_TRANSITION_DIR, "counter_sel.png"),
        "hover": os.path.join(IN_TRANSITION_DIR, "counter_hover.png")
    },
    "hold shape": {
        "unselected": os.path.join(IN_TRANSITION_DIR, "hold_shape_un.png"),
        "selected": os.path.join(IN_TRANSITION_DIR, "hold_shape_sel.png"),
        "hover": os.path.join(IN_TRANSITION_DIR, "hold_shape_hover.png")
    }
}

# Mentalities Images
MENTALITY_IMAGES = {
    'attacking': os.path.join(BASE_IMAGE_DIR, "mentalities", "current", "attacking_current.png"),
    'balanced': os.path.join(BASE_IMAGE_DIR, "mentalities", "current", "balanced_current.png"),
    'defensive': os.path.join(BASE_IMAGE_DIR, "mentalities", "current", "defensive_current.png"),
    'very defensive': os.path.join(BASE_IMAGE_DIR, "mentalities", "current", "very_defensive_current.png"),
    'positive': os.path.join(BASE_IMAGE_DIR, "mentalities", "current", "positive_current.png"),
    'cautious': os.path.join(BASE_IMAGE_DIR, "mentalities", "current", "cautious_current.png"),
    'very attacking': os.path.join(BASE_IMAGE_DIR, "mentalities", "current", "very_attacking_current.png"),
}

TARGET_MENTALITY_IMAGES = {
    'attacking': os.path.join(BASE_IMAGE_DIR, "mentalities", "attacking_mentality.png"),
    'balanced': os.path.join(BASE_IMAGE_DIR, "mentalities", "Balanced_mentality.png"),
    'defensive': os.path.join(BASE_IMAGE_DIR, "mentalities", "defensive_mentality.png"),
    'very defensive': os.path.join(BASE_IMAGE_DIR, "mentalities", "Very_defensive_mentality.png"),
    'positive': os.path.join(BASE_IMAGE_DIR, "mentalities", "Positive_mentality.png"),
    'cautious': os.path.join(BASE_IMAGE_DIR, "mentalities", "cautious_mentality.png"),
    'very attacking': os.path.join(BASE_IMAGE_DIR, "mentalities", "Very_attacking_mentality.png"),
}

# Shouts Images
SHOUTS_BUTTON_IMAGE = os.path.join(BASE_IMAGE_DIR, "Shouts", "Shouts_menu.png")
SHOUT_IMAGES = {
    'encourage': os.path.join(BASE_IMAGE_DIR, "Shouts", "encourage.png"),
    'calm down': os.path.join(BASE_IMAGE_DIR, "Shouts", "calm_down.png"),
    'focus': os.path.join(BASE_IMAGE_DIR, "Shouts", "Focus.png"),
    'fire up': os.path.join(BASE_IMAGE_DIR, "Shouts", "fire_up.png"),
    'no pressure': os.path.join(BASE_IMAGE_DIR, "Shouts", "no_pressure.png"),
    'demand more': os.path.join(BASE_IMAGE_DIR, "Shouts", "demand_more.png"),
    'praise': os.path.join(BASE_IMAGE_DIR, "Shouts", "Praise.png"),
    'berate': os.path.join(BASE_IMAGE_DIR, "Shouts", "berate.png"),
}

# Instructions Images
INSTRUCTIONS_IMAGES = {
    "hit early crosses": {
        "unselected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "hit_early_crosses_un.png"),
        "selected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "hit_early_crosses_sel.png")
    },
    "pass into space": {
        "unselected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "pass_into_space_un.png"),
        "selected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "pass_into_space_sel.png")
    },
    "shoot on sight": {
        "unselected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "shoot_on_sight_un.png"),
        "selected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "shoot_on_sight_sel.png")
    },
    "work ball into box": {
        "unselected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "work_the_ball_into_box_un.png"),
        "selected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "work_the_ball_into_box_sel.png")
    },
    "be more expressive": {
        "unselected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "be_more_expressive_un.png"),
        "selected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "be_more_expressive_sel.png")
    },
    "be more disciplined": {
        "unselected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "be_more_disciplined_un.png"),
        "selected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "be_more_disciplined_sel.png")
    },
    "play for set pieces": {
        "unselected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "play_for_set_pieces_un.png"),
        "selected": os.path.join(BASE_IMAGE_DIR, "instructions", "in_possession", "play_for_set_pieces_sel.png")
    }
}

# Substitution Images
SUBSTITUTIONS_DIR = os.path.join(BASE_IMAGE_DIR, "substitutions")
SUBSTITUTIONS_MENU_IMAGE = os.path.join(SUBSTITUTIONS_DIR, "substitutions_menu.png")
CONFIRM_SUB_BUTTON = os.path.join(SUBSTITUTIONS_DIR, "confirm_sub.png")

# Substitution buttons
SUBSTITUTE_IMAGES = {
    "S1": os.path.join(SUBSTITUTIONS_DIR, "S1.png"),
    "S2": os.path.join(SUBSTITUTIONS_DIR, "S2.png"),
    "S3": os.path.join(SUBSTITUTIONS_DIR, "S3.png"),
    "S4": os.path.join(SUBSTITUTIONS_DIR, "S4.png"),
    "S5": os.path.join(SUBSTITUTIONS_DIR, "S5.png"),
    "S6": os.path.join(SUBSTITUTIONS_DIR, "S6.png"),
    "S7": os.path.join(SUBSTITUTIONS_DIR, "S7.png"),
    "S8": os.path.join(SUBSTITUTIONS_DIR, "S8.png"),
    "S9": os.path.join(SUBSTITUTIONS_DIR, "S9.png"),
    "S10": os.path.join(SUBSTITUTIONS_DIR, "S10.png"),
    "S11": os.path.join(SUBSTITUTIONS_DIR, "S11.png"),
    "S12": os.path.join(SUBSTITUTIONS_DIR, "S12.png")
}

# Position buttons
POSITIONS_DIR = os.path.join(SUBSTITUTIONS_DIR, "positions")
POSITION_BUTTONS = {
    'GK': os.path.join(POSITIONS_DIR, "GK.png"),
    'DR': os.path.join(POSITIONS_DIR, "DR.png"),
    'DCR': os.path.join(POSITIONS_DIR, "DCR.png"),
    'DCL': os.path.join(POSITIONS_DIR, "DCL.png"),
    'DL': os.path.join(POSITIONS_DIR, "DL.png"),
    'MCR': os.path.join(POSITIONS_DIR, "MCR.png"),
    'MC': os.path.join(POSITIONS_DIR, "MC.png"),
    'MCL': os.path.join(POSITIONS_DIR, "MCL.png"),
    'AMR': os.path.join(POSITIONS_DIR, "AMR.png"),
    'AML': os.path.join(POSITIONS_DIR, "AML.png"),
    'STC': os.path.join(POSITIONS_DIR, "STC.png")
}

# Game Control Images
PAUSE_BUTTON_IMAGE = os.path.join(BASE_IMAGE_DIR, "pause.png")
RESUME_BUTTON_IMAGE = os.path.join(BASE_IMAGE_DIR, "resume.png")

# Natural position names and their mappings
POSITION_MAPPINGS = {
    # Goalkeeper
    "goalkeeper": "GK",
    "keeper": "GK",
    "goalie": "GK",
    "goalkeeper position": "GK",
    "keeper position": "GK",
    "goalie position": "GK",
    
    # Defenders
    "right defender": "DR",
    "right back": "DR",
    "right fullback": "DR",
    "right wingback": "DR",
    "right side defender": "DR",
    "right side back": "DR",
    
    "right center defender": "DCR",
    "right center back": "DCR",
    "right central defender": "DCR",
    "right center half": "DCR",
    "right stopper": "DCR",
    
    "center defender": "DC",
    "center back": "DC",
    "central defender": "DC",
    "center half": "DC",
    "stopper": "DC",
    "defender": "DC",
    
    "left center defender": "DCL",
    "left center back": "DCL",
    "left central defender": "DCL",
    "left center half": "DCL",
    "left stopper": "DCL",
    
    "left defender": "DL",
    "left back": "DL",
    "left fullback": "DL",
    "left wingback": "DL",
    "left side defender": "DL",
    "left side back": "DL",
    
    # Midfielders
    "right center midfielder": "MCR",
    "right central midfielder": "MCR",
    "right midfielder": "MCR",
    "right side midfielder": "MCR",
    "right wing midfielder": "MCR",
    "right attacking midfielder": "MCR",
    
    "center midfielder": "MC",
    "central midfielder": "MC",
    "midfielder": "MC",
    "center mid": "MC",
    "central mid": "MC",
    "mid": "MC",
    
    "left center midfielder": "MCL",
    "left central midfielder": "MCL",
    "left midfielder": "MCL",
    "left side midfielder": "MCL",
    "left wing midfielder": "MCL",
    "left attacking midfielder": "MCL",
    
    # Attacking Midfielders
    "right attacking midfielder": "AMR",
    "right winger": "AMR",
    "right wing": "AMR",
    "right forward": "AMR",
    "right inside forward": "AMR",
    "right wide midfielder": "AMR",
    
    "left attacking midfielder": "AML",
    "left winger": "AML",
    "left wing": "AML",
    "left forward": "AML",
    "left inside forward": "AML",
    "left wide midfielder": "AML",
    
    # Forwards
    "striker": "STC",
    "forward": "STC",
    "center forward": "STC",
    "target man": "STC",
    "number 9": "STC",
    "center striker": "STC",
    "central striker": "STC",
    "main striker": "STC",
    "primary striker": "STC"
}

# Game commands
MENTALITIES = [
    "very defensive",
    "defensive",
    "cautious",
    "balanced",
    "positive",
    "attacking",
    "very attacking"
]

SHOUTS = [
    "encourage",
    "calm down",
    "focus",
    "fire up",
    "no pressure",
    "demand more",
    "praise",
    "berate"
]

INSTRUCTIONS = [
    "hit early crosses",
    "pass into space",
    "shoot on sight",
    "work ball into box",
    "be more expressive",
    "be more disciplined",
    "play for set pieces"
]

IN_TRANSITION_INSTRUCTIONS = [
    "counter press",
    "regroup",
    "counter",
    "hold shape"
]

ENGAGEMENT_POSITIONS = [
    "high press",
    "high block",
    "press high",
    "higher press",
    "mid block",
    "middle block",
    "medium block",
    "low block",
    "drop deep",
    "low engagement",
    "low press",
    "lower press",
    "low pressure",
    "lower pressure"
]

DEFENSIVE_LINE_POSITIONS = [
    "much higher defensive line",
    "much higher defense",
    "higher defensive line",
    "higher defense",
    "standard defensive line",
    "normal defensive line",
    "lower defensive line",
    "lower defense",
    "much lower defensive line",
    "much lower defense"
] 