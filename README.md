## Project FM - Voice Control for Football Manager

A powerful voice-controlled assistant for Football Manager that lets you make tactical changes with your voice. Perfect for making quick adjustments during matches without taking your hands off the keyboard.

## 🚀 Quick Start Guide

1. **Install the program** (see Installation section below)
2. **Start the program**:
   ```bash
   python src/core/main.py
   ```
3. **Basic Controls**:
   - Hold `Caps Lock` to speak commands
   - Press `T` to type commands instead
   - Press `Space` to pause/resume the game
   - Press `Q` to quit

4. **Try these simple commands first**:
   ```
   "Switch to attacking mentality"
   "Encourage the team"
   "Hit early crosses"
   ```

## 🎯 Key Features

### Multiple Commands in One Go
The best part? You can combine multiple commands in a single sentence! The program will execute them in the right order.

**Try these examples:**
```
"Go attacking, hit early crosses,substitute right center back with sub 2  and encourage the team"
"Switch to balanced, pass into space, and work ball into box"
"Go defensive, regroup, and calm down the team"
```

### Available Commands

#### 🧠 Team Mentalities
- "Go very defensive"
- "Switch to defensive"
- "Change to balanced"
- "Go positive"
- "Switch to attacking"
- "Go very attacking"

#### 📢 Team Shouts
- "Encourage the team"
- "Calm down the team"
- "Tell them to focus"
- "Fire up the team"
- "Say no pressure"
- "Demand more from them"
- "Praise the team"
- "Berate the team"

#### ⚽ In-Possession Instructions
- "Hit early crosses"
- "Pass into space"
- "Shoot on sight"
- "Work ball into box"
- "Be more expressive"
- "Be more disciplined"
- "Play for set pieces"

#### 🔄 In-Transition Instructions
- "Counter press"
- "Regroup"
- "Counter"
- "Hold shape"

#### 🔄 Substitutions
- "Substitute [player] with [substitute]"
- "Bring on [substitute] for [player]"
- "Swap [player1] with [player2]"
- "Change [player]'s position to [position]"
- "Make a triple substitution: [player1] off, [sub1] on; [player2] off, [sub2] on; [player3] off, [sub3] on"

## 💡 Tips for Best Results

1. **Speak clearly and naturally**
   - Don't rush your commands
   - Use normal speaking pace
   - The program understands natural language

2. **Combine commands effectively**
   - Use "and" or commas to separate commands
   - Example: "Go attacking and hit early crosses"

3. **Common phrases that work well**
   - "Switch to [mentality]"
   - "Go [mentality]"
   - "Change to [mentality]"
   - "Tell them to [shout]"
   - "Make them [instruction]"

## 🛠️ Installation

1. **Download the program**:
   ```bash
   git clone https://github.com/yourusername/projectfm.git
   cd projectfm
   ```

2. **Install required software**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**:
   - Download from [here](https://github.com/UB-Mannheim/tesseract/wiki)
   - Follow the installation instructions
   - Make sure it's added to your system PATH

4. **Set up Azure Speech Services**:
   - Create an Azure account
   - Get your Speech Services key
   - Update the settings in `src/core/config.py`

## 🎮 Game Controls

- `Caps Lock`: Hold to speak commands
- `T`: Switch to text command mode
- `P`: Read player positions and roles
- `Space`: Pause/resume the game
- `Q`: Quit the program

## 📚 Example Scenarios

### When You're Losing
```
"Go attacking, pass into space, and fire up the team"
```

### When You're Winning
```
"Go defensive, regroup, and calm down the team"
```

### When You Need a Goal
```
"Switch to very attacking, shoot on sight, and encourage the team"
```

### When Defending a Lead
```
"Go very defensive, hold shape, and tell them to focus"
```

### Making Substitutions
```
"Substitute John Smith with David Johnson"
"Bring on Michael Brown for tired James Wilson"
"Swap left back with right back"
"Change striker to attacking midfielder"
```

### Multiple Substitutions
```
"Make two substitutions: bring on Johnson for Smith and Brown for Wilson"
"Triple substitution: Smith off, Johnson on; Wilson off, Brown on; Davis off, Taylor on"
```

### Position Changes
```
"Change Johnson to right back"
"Move Smith to attacking midfield"
"Switch Wilson to striker"
```

### Combined Tactics and Substitutions
```
"Go attacking, bring on fresh legs: Johnson for Smith, and encourage the team"
"Switch to defensive, make two changes: Brown for Wilson and Taylor for Davis, then regroup"
```

## 🤝 Contributing

Want to help improve Project FM? Here's how:
1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Thanks to:
- Football Manager for the amazing game
- Azure Speech Services for voice recognition
- Tesseract OCR for reading game text 
