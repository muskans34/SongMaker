import os
import numpy as np
from pydub import AudioSegment
import pyttsx3


def text_to_speech(text, output_file, voice='default'):
    engine = pyttsx3.init()

    # Set the voice
    voices = engine.getProperty('voices')
    if voice == 'male':
        engine.setProperty('voice', voices[0].id)  # Select the first male voice
    elif voice == 'female':
        engine.setProperty('voice', voices[1].id)  # Select the first female voice

    engine.save_to_file(text, output_file)
    engine.runAndWait()


def generate_song(lyrics_file, karaoke_file, output_file, voice='default'):
    with open(lyrics_file, 'r') as f:
        lyrics = f.read()

    speech_file = "speech.wav"
    text_to_speech(lyrics, speech_file, voice=voice)

    karaoke = AudioSegment.from_file(karaoke_file)

    speech = AudioSegment.from_file(speech_file)
    generated_song = karaoke.overlay(speech)

    generated_song.export(output_file, format='mp3')
    print("Song generated successfully!")


if __name__ == "__main__":
    lyrics_file = input("Enter path to lyrics file: ")
    karaoke_file = input("Enter path to karaoke track: ")
    output_file = input("Enter path for output song: ")
    voice = input("Enter voice preference (male/female/default): ").lower()

    generate_song(lyrics_file, karaoke_file, output_file, voice=voice)

# "C:\Users\Muskan\Desktop\lyrics.txt"
# "C:\Users\Muskan\Desktop\k3g.mp3"