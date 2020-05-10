""" проигрывает слово при помощи спец утилиты"""
from gtts import gTTS
from playsound import playsound
import os
from datetime import *


def play(word_name, language):
    myobj = gTTS(text = word_name, lang = language, slow = False)
    d = datetime.now()
    string = str(d.strftime("(%d)(%m)(%Y)(%H)(%M)(%S)"))
    path = f"{string}.mp3"
    myobj.save(path)
    playsound(path)
    os.remove(path)


if __name__ == '__main__':
    play("empty space", "en")
