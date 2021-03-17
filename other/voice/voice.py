# coding=utf-8
import pyttsx
# import pyttsx3

engine = pyttsx.init()
engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0")
engine.say("Good")
# engine.say("你好吗？")
engine.runAndWait()
