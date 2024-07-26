# cli.py
from blessed import Terminal
import os
import inquirer
from inquirer.themes import GreenPassion, Default
from Backend import TTS, Static, CleanUp, Dynamic, Custom


def UI():
    if os.name == "nt":
        os.system("cls")
    print(
        """
  __               _    
 /  )       _/  ' (_    
(__\  (/ () /  /  /  (/ 
                     /  
    """
    )
    questions = [
        inquirer.List(
            "command",
            message="What would you want to do?",
            choices=["Custom", "Dynamic", "Static", "TTS", "Clean Up"],
        ),
    ]

    answers = inquirer.prompt(questions, theme=HighQuality())

    if answers["command"] == "Custom":
        speakers = [
            f
            for f in os.listdir("./Speakers")
            if os.path.isfile(os.path.join("./Speakers", f))
        ]
        speakers = [speaker.replace(".wav", "") for speaker in speakers]
        music_genres = [
            f
            for f in os.listdir("./Music")
            if os.path.isdir(os.path.join("./Music", f))
        ]
        backgrounds = [
            f
            for f in os.listdir("./Background")
            if os.path.isfile(os.path.join("./Background", f))
        ]

        custom_questions = [
            inquirer.Text("quote", message="Enter the quote to convert to speech"),
            inquirer.Text("author", message="Author of the quote"),
            inquirer.List("speaker", message="Choose a speaker", choices=speakers),
            inquirer.List(
                "background", message="Choose background footage", choices=backgrounds
            ),
            inquirer.Confirm(
                "attribution", message="Do you want attribution?", default=True
            ),
        ]

        custom_answers = inquirer.prompt(custom_questions, theme=HighQuality())

        music_questions = [
            inquirer.List(
                "music", message="Choose a music genre", choices=music_genres
            ),
        ]
        music_genre_answers = inquirer.prompt(music_questions, theme=HighQuality())
        music_questions = [
            inquirer.List(
                "music file",
                message="Choose a music file",
                choices=os.listdir(f"./Music/{music_genre_answers['music']}"),
            ),
        ]
        music_answers = inquirer.prompt(music_questions, theme=HighQuality())
        Custom(
            custom_answers["quote"],
            custom_answers["author"],
            custom_answers["speaker"],
            f"./Music/{music_genre_answers['music']}/{music_answers['music file']}",
            f"./Background/{custom_answers['background']}",
            custom_answers["attribution"],
        )
        if os.name == "nt":
            os.system("cls")

    elif answers["command"] == "Dynamic":
        speakers = [
            f
            for f in os.listdir("./Speakers")
            if os.path.isfile(os.path.join("./Speakers", f))
        ]
        speakers = [speaker.replace(".wav", "") for speaker in speakers]
        dynamic_questions = [
            inquirer.List("speaker", message="Choose a speaker", choices=speakers),
            inquirer.Confirm(
                "attribution", message="Do you want attribution?", default=True
            ),
        ]
        dynamic_answers = inquirer.prompt(dynamic_questions, theme=HighQuality())
        Dynamic(dynamic_answers["speaker"], dynamic_answers["attribution"])
        if os.name == "nt":
            os.system("cls")

    elif answers["command"] == "Static":
        speakers = [
            f
            for f in os.listdir("./Speakers")
            if os.path.isfile(os.path.join("./Speakers", f))
        ]
        speakers = [speaker.replace(".wav", "") for speaker in speakers]
        static_questions = [
            inquirer.List("speaker", message="Choose a speaker", choices=speakers),
            inquirer.Confirm(
                "attribution", message="Do you want attribution?", default=True
            ),
        ]
        static_answers = inquirer.prompt(static_questions, theme=HighQuality())
        Static(static_answers["speaker"], static_answers["attribution"])
        if os.name == "nt":
            os.system("cls")

    elif answers["command"] == "TTS":
        speakers = [
            f
            for f in os.listdir("./Speakers")
            if os.path.isfile(os.path.join("./Speakers", f))
        ]
        speakers = [speaker.replace(".wav", "") for speaker in speakers]
        tts_questions = [
            inquirer.Text("text", message="Text to convert to speech"),
            inquirer.List("speaker", message="Choose a speaker", choices=speakers),
            inquirer.Text("filename", message="Output filename"),
        ]
        tts_answers = inquirer.prompt(tts_questions, theme=HighQuality())
        if tts_answers["filename"] == "":
            tts_answers["filename"] = "./WAVFILES/TTS.wav"
        elif not tts_answers["filename"].endswith(".wav"):
            tts_answers["filename"] = f"{tts_answers['filename']}.wav"
        
        TTS(tts_answers["text"], tts_answers["speaker"], tts_answers["filename"])
        if os.name == "nt":
            os.system("cls")

    elif answers["command"] == "Clean Up":
        CleanUp()
        if os.name == "nt":
            os.system("cls")


class HighQuality(Default):
    def __init__(self):
        super().__init__()
        self.Question.brackets_color = Terminal().bright_blue
        self.Checkbox.selection_color = Terminal().bold_white_on_bright_blue
        self.Checkbox.selection_icon = "❯"
        self.Checkbox.selected_icon = "◉"
        self.Checkbox.selected_color = Terminal().blue
        self.Checkbox.unselected_icon = "◯"
        self.List.selection_color = Terminal().bold_white_on_bright_blue
        self.List.selection_cursor = "❯"


if __name__ == "__main__":
    UI()
