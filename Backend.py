import logging
import os
import random
import ffmpeg
import subprocess
import pathlib
from typing import List, Dict
import pathlib
import json
import requests



def TTS(text: str, speaker: str, filename: str):
    if pathlib.Path(filename).exists():
        return
    try:
        os.system(
            f'tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 --text "{text}" --speaker_wav ./Speakers/{speaker}.wav --language_idx en --use_cuda true --out_path "{filename}"'
        )
    except:
        logging.error("An error occurred while executing the TTS command.")
        return ""


def DownloadMusic(folder: str) -> None:
    if folder not in PLAYLISTS:
        raise ValueError(f"Invalid folder: {folder}")

    try:
        result = subprocess.run(
            ["yt-dlp", "--flat-playlist", "-J", PLAYLISTS[folder]],
            capture_output=True,
            text=True,
            check=True,
        )

        playlist_info = json.loads(result.stdout)
        videos = playlist_info["entries"]
        while videos:
            random_video = random.choice(videos)
            random_video_url = f"https://www.youtube.com/watch?v={random_video['id']}"

            options = [
                "yt-dlp",
                "-f",
                "bestaudio[ext=m4a],bestaudio[ext=webm]",
                "-x",
                "--audio-format",
                "mp3",
                "--output",
                f"./Music/{folder} Music/%(title)s.%(ext)s",
            ]
            options.append(random_video_url)

            try:
                subprocess.run(options, check=True)
                break  # Exit the loop if download is successful
            except subprocess.CalledProcessError as e:
                logging.error(f"An error occurred with video {random_video_url}: {e}")

        if not videos:
            logging.error("No valid videos found in the playlist.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def DynamicPoems():
    urls = [
        "https://zenquotes.io/api/random",
        "https://programming-quotesapi.vercel.app/api/random",
    ]

    dynamicPoems = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if url == "https://zenquotes.io/api/random":
                dynamicPoems.append(
                    {
                        "genre": "General",
                        "quote": data[0]["q"],
                        "author": data[0]["a"],
                    }
                )
            elif url == "https://programming-quotesapi.vercel.app/api/random":
                dynamicPoems.append(
                    {
                        "genre": "Programming",
                        "quote": data["quote"],
                        "author": data["author"],
                    }
                )
        else:
            dynamicPoems.append("Error fetching poem from " + url)

    return dynamicPoems


global DBPATH
DBPATH = os.path.join(os.getcwd(), "DB")
global WAVPATH
WAVPATH = pathlib.Path(os.path.join(os.getcwd(), "WAVFILES"))
global PLAYLISTS
PLAYLISTS = {
    "Anime": "https://www.youtube.com/watch?v=BpcdiYYEmvE&list=PLl578ZPbYIlFcSxuka8Km37VgbUYUWI5p",
    "General": "https://www.youtube.com/watch?v=P9J93t1k418&list=PLbPqG08ImzRhcK_7H53Qn2DwtbqeysQj3",
    "Programming": "https://www.youtube.com/watch?v=uJv3YCk9wD4&list=PLPmlXT-rSvsrniYJ7dq5bsWI5jzoDabvt",
}


def StaticPoems() -> Dict[str, Dict[str, str]]:
    folder_quotes: Dict[str, List[Dict[str, str]]] = {}

    for path in pathlib.Path(DBPATH).iterdir():
        if path.is_dir():
            folder_quotes[path.name] = []

            for file_path in path.iterdir():
                if file_path.suffix == ".json":
                    try:
                        with file_path.open("r", encoding="utf-8") as file:
                            data = json.load(file)

                            if isinstance(data, (dict, list)):
                                if isinstance(data, dict):
                                    data = [data]

                                for item in data:
                                    if isinstance(item, dict):
                                        quote = item.get("quote", "")
                                        author = item.get("author", "")
                                        if quote and author:
                                            folder_quotes[path.name].append(
                                                {"quote": quote, "author": author}
                                            )

                    except (IOError, json.JSONDecodeError) as e:
                        logging.error(f"Error reading {file_path}: {e}")

    staticPoems = {
        folder: random.choice(quotes)
        for folder, quotes in folder_quotes.items()
        if quotes
    }

    return staticPoems


def CreateVideo(
    wav: str,
    subtitles: str,
    title: str,
    genre: str,
    music: str,
    background: str,
    custom: bool,
):
    if not custom:
        MUSIC = os.path.join(
            "Music",
            f"{genre} Music",
            random.choice(os.listdir(os.path.join("Music", f"{genre} Music"))),
        )
        BACKGROUND = f"./Background/{random.choice(os.listdir('./Background/'))}"
    else:
        MUSIC = music
        BACKGROUND = background
    title = f'{title[:20]} - {title.split(" - ", 1)[1]}'
    try:
        wavInfo = ffmpeg.probe(wav)
        videoInfo = ffmpeg.probe(BACKGROUND)
        musicInfo = ffmpeg.probe(MUSIC)
    except Exception as e:
        logging.error(f"Error probing files: {e}")
        return

    wavDuration = float(wavInfo["streams"][0]["duration"])
    videoDuration = float(videoInfo["streams"][0]["duration"])
    musicDuration = float(musicInfo["streams"][0]["duration"])

    repeat = int(wavDuration / videoDuration) + 1

    loop_filter = f"loop={repeat}:size=1:start=0"
    filter_complex = (
        f"[0:v]{loop_filter},subtitles={subtitles}:force_style='Fontname=Gabriola,FontSize=24,PrimaryColour=&H00FFFFFF&,OutlineColour=&H00000000&,BackColour=&H80000000&,BorderStyle=1,Outline=1.1,Shadow=1.5,Alignment=10',"
        "setsar=1,eq=brightness=0.1:contrast=1.3[v];"
        "[1:a][2:a]amix=inputs=2:duration=longest[a]"
    )

    command = [
        "ffmpeg",
        "-stream_loop",
        str(repeat - 1),
        "-i",
        BACKGROUND,
        "-i",
        wav,
        "-i",
        MUSIC,
        "-y",
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-b:v",
        "2M",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-t",
        str(wavDuration),  # Trim the output to the duration of the .wav file
        f"./Videos/{genre} Videos/{title}.mp4",
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing ffmpeg command: {e}")


def CleanUp():
    try:
        for root, _, files in os.walk("./Music"):
            for file in files:
                if root == "./Music\Custom Music":
                    continue
                else:
                    os.remove(os.path.join(root, file))
        for root, _, files in os.walk("./Subtitles"):
            for file in files:
                os.remove(os.path.join(root, file))
        for root, _, files in os.walk("./WAVFILES"):
            for file in files:
                os.remove(os.path.join(root, file))
    except Exception as e:
        logging.error(f"An error occurred during cleanup: {e}")


def GetAttribution(quote, author):
    attributes = [
        f"{author} once said,",
        f"{author} said,",
        f"{author} once told me,",
        f"A life quote from {author},",
        f"A life quote by {author},",
        f"A life lesson from {author},",
        f"A life lesson by {author},",
        f"A quote from {author},",
        f"A quote by {author},",
        f"How beautiful it was when {author} said,",
    ]
    return random.choice(attributes) + " " + quote


def Subtitles(filename: str):
    if not os.path.exists(
        f'./Subtitles/{filename.replace("WAVFILES/", "").replace(".wav", "")}.srt'
    ):
        try:
            subprocess.run(
                [
                    "auto_subtitle_llama",
                    f"{filename}",
                    "--model",
                    "medium",
                    "-o",
                    "./Subtitles/",
                    "--srt_only",
                    "True",
                ]
            )
        except:
            print("Error generating subtitles on video")
    else:
        return


def Custom(quote, author, speaker, music, background, attribution):
    if attribution:
        quote = GetAttribution(quote, author)
    filename = f"./WAVFILES/Custom{author.replace(' ', '')}.wav"
    TTS(quote, speaker, str(filename))
    Subtitles(filename)
    CreateVideo(
        filename,
        f"./Subtitles/{filename.replace('WAVFILES/', '').replace('.wav', '')}.srt",
        f"{quote} - {author}",
        "Custom",
        music,
        background,
        True,
    )


def Dynamic(speaker, attribution: bool):
    DYNAMIC = DynamicPoems()
    for poem in DYNAMIC:
        quote: str = poem["quote"]
        author = poem["author"]
        if attribution:
            quote = GetAttribution(quote, author)
        filename = f"./WAVFILES/General{author.replace(' ', '')}.wav"
        TTS(quote, speaker, str(filename))
        Subtitles(filename)
        DownloadMusic(poem["genre"])
        CreateVideo(
            filename,
            f"./Subtitles/{filename.replace('WAVFILES/', '').replace('.wav', '')}.srt",
            f"{quote} - {author}",
            poem["genre"],
            "",
            "",
            False,
        )


def Static(speaker, attribution: bool):
    STATIC = StaticPoems()
    for folder, poem in STATIC.items():
        quote = poem["quote"]
        author = poem["author"]
        if isinstance(author, list) and len(author) > 0:
            author = author[0]
        if attribution:
            quote = GetAttribution(quote, author)
        filename = f"./WAVFILES/{folder.replace(' ', '')}{author.replace(' ', '')}.wav"
        TTS(quote, speaker, str(filename))
        STATIC[folder]["filename"] = str(filename)

        Subtitles(filename)

        DownloadMusic(folder.replace(" Quotes", ""))
        CreateVideo(
            STATIC[folder]["filename"],
            f"./Subtitles/{filename.replace('WAVFILES/', '').replace('.wav', '')}.srt",
            f"{quote} - {author}",
            folder.replace(" Quotes", ""),
            "",
            "",
            False,
        )


"""
TODO:
Notion Intergration

"""
