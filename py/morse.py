from pydub import AudioSegment
from pydub.generators import Sine
from mylib import morse_code_dict

def text_to_morse(text):
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
message = "Es ist nicht tot, was ewig liegt, bis das die Zeit den Tod besiegt"
print(convert_text_to_morse_audio(message))
