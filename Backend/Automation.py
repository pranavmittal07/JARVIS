from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

load_dotenv()

Groq_API_Key = os.getenv("GROQ_API_KEY")
username = os.getenv("username")

if not Groq_API_Key or not username:
    raise ValueError("Ensure that GROQ_API_KEY and username are set in the .env file.")

classes = [
    "zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
    "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d",
    "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e",
    "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0142.86 Safari/537.36"
client = Groq(api_key=Groq_API_Key)

messages = []
SystemChat = [{"role": "system", "content": f"Hello, I am {username}, you're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems, etc."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model='mistral-8x7b-32768',
            messages=SystemChat + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        answer = answer.replace("<s>", "")
        messages.append({"role": "assistant", "content": answer})
        return answer

    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    os.makedirs("Data", exist_ok=True)
    file_path = rf"Data\{Topic.lower().replace(' ', '')}.txt"
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(ContentByAI)

    OpenNotepad(file_path)
    return True

def YouTubeSearch(Topic):
    url4search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(url4search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, "html.parser")
            links = soup.find_all("a", {"jsname": "UWckNb"})
            return [link["href"] for link in links]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": user_agent}
            response = sess.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            else:
                print("Failed to search Google")
            return None

        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                webopen(links[0])
                return True
            else:
                print("No links found")

        return False

def CloseApp(app):
    if "chrome" in app:
        return False
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

def System(command):
    def mute():
        keyboard.press_and_release("volume mute")
        return True

    def unmute():
        keyboard.press_and_release("volume mute")
        return True

    def volumeup():
        keyboard.press_and_release("volume up")
        return True

    def volumedown():
        keyboard.press_and_release("volume down")
        return True

    if command == "mute":
        return mute()
    elif command == "unmute":
        return unmute()
    elif command == "volume up":
        return volumeup()
    elif command == "volume down":
        return volumedown()
    return False

async def TranslateAndExecute(commands: list[str]):
    func = []

    for command in commands:
        if command.startswith("open "):
            fun = asyncio.to_thread(OpenApp, command.replace("open ", ""))
            func.append(fun)
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.replace("close ", ""))
            func.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.replace("play ", ""))
            func.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command)
            func.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command)
            func.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command)
            func.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.replace("system ", ""))
            func.append(fun)
        else:
            print(f"No Function Found for {command}")

    results = await asyncio.gather(*func)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True


if __name__ == "__main__":
    asyncio.run(Automation(["open notepad", "content Content Write a letter to your friend about your favourite hobby.", "close notepad"]))