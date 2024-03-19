"""
Script Name: morse.py
Description: This script converts plain text to Morse code and then generates an audio representation of that Morse code using the pydub library. It supports conversion from alphanumeric characters to Morse and can be used to create audio files for Morse code training, alerts, or other applications.

Functions:
    text_to_morse(text) - Converts a text string to its Morse code representation using a predefined dictionary.
    morse_to_audio(morse_code, filename="morse_sound.wav") - Converts a Morse code string to an audio file, with customizable parameters for tone frequency and durations of Morse code elements.

Usage:
    1. Convert text to Morse code using the text_to_morse function.
    2. Generate an audio file from the Morse code string using the morse_to_audio function.
    3. The generated audio file will be saved with the specified filename, defaulting to 'morse_sound.wav'.
"""


from pydub import AudioSegment
from pydub.generators import Sine

def text_to_morse(text):
    morse_code_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
        'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', 
        '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
        '9': '----.', '0': '-----'
    }
    return ' '.join(morse_code_dict.get(char.upper(), '') for char in text if char.isalpha() or char.isdigit())

def morse_to_audio(morse_code, filename="morse_sound.wav"):
    frequency = 500
    intDurationShort = 50
    intDurationLong = 150
    intDurationPause = 300
    intDurationNo = 0

    dot = Sine(frequency).to_audio_segment(intDurationShort)
    dash = Sine(frequency).to_audio_segment(intDurationLong)
    gap = AudioSegment.silent(intDurationShort)
    medium_gap = AudioSegment.silent(intDurationLong)
    long_gap = AudioSegment.silent(intDurationPause)

    audio = AudioSegment.silent(intDurationNo)
    for symbol in morse_code:
        if symbol == '.':
            audio += dot + gap
        elif symbol == '-':
            audio += dash + gap
        elif symbol == ' ':
            audio += medium_gap
        else:
            audio += long_gap

    audio.export(filename, format="wav")
    return filename

def convert_text_to_morse_audio(text):
    morse = text_to_morse(text)
    audio_file = morse_to_audio(morse)
    return f"Text: {text}\nMorsecode: {morse}\nAudio-Datei: {audio_file}"

# Beispiel der Nutzung
message = "Es ist nicht tot, was ewig liegt, auf das der Schlaf den Tod besiegt"
print(convert_text_to_morse_audio(message))
