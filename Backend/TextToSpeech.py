import pygame
import random
import asyncio
import edge_tts
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

assistant_voice = os.getenv("ASSISTANT_VOICE")
if not assistant_voice:
    raise ValueError("ASSISTANT_VOICE is not defined in the .env file.")

# Asynchronous function to generate TTS audio file
async def TextToAudioFile(text) -> None:
    file_path = os.path.join('Data', 'speech.mp3')
    if os.path.exists(file_path):
        os.remove(file_path)

    communicate = edge_tts.Communicate(text, assistant_voice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

# Function to play TTS audio
def TTS(Text, func=lambda r=None: True):
    try:
        asyncio.run(TextToAudioFile(Text))
        pygame.mixer.init()

        file_path = os.path.join('Data', 'speech.mp3')
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if func() == False:
                break
            pygame.time.Clock().tick(10)

        return True
    except Exception as e:
        print(f'Error in TTS: {e}')
    finally:
        try:
            func(False)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f'Error in finally block: {e}')

# Main Text-to-Speech function with response handling
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split('.')
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out.",
        "You can see the rest of the text on the chat screen.",
        "The remaining part of the text is now on the chat screen.",
        "Please check the chat screen for more information.",
        "The chat screen has the rest of the text.",
    ]

    if len(Data) > 4 and len(Text) > 250:
        TTS(" ".join(Data[:2]) + ". " + random.choice(responses), func)
    else:
        TTS(Text, func)

# Main program loop
if __name__ == "__main__":
    while True:
        user_input = input("Enter the Text (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break
        TextToSpeech(user_input)

