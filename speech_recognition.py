import azure.cognitiveservices.speech as speechsdk
from config import AZURE_SPEECH_KEY, AZURE_REGION

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