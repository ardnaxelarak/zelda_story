import codecs
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from story import generate

ScriptName = "Zelda Storyteller"
Website = "http://www.github.com/ardnaxelarak/zelda_story"
Description = "Tell Zelda-themed stories for Streamlabs Bot"
Creator = "karafruit"
Version = "1.0.0"

configFile = "config.json"
settings = {}

def ScriptToggled(state):
    return

def Init():
    global settings

    try:
        with codecs.open(os.path.join(os.path.dirname(__file__), configFile), encoding='utf-8-sig', mode='r') as file:
            settings = json.load(file, encoding='utf-8-sig')
    except:
        settings = {
            "liveOnly": True,
            "command": "!story",
            "permission": "Everyone",
            "useCooldown": True,
            "useCooldownMessages": True,
            "cooldown": 300,
            "onCooldown": "$user, $command is still on cooldown for $cd seconds!",
            "userCooldown": 10,
            "onUserCooldown": "$user, $command is still on user cooldown for $cd seconds!",
        }


def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, settings["permission"], "") and (not settings["liveOnly"] or Parent.IsLive()):
        outputMessage = ""
        userId = data.User
        username = data.UserName

        if settings["useCooldown"] and (Parent.IsOnCooldown(ScriptName, settings["command"]) or Parent.IsOnUserCooldown(ScriptName, settings["command"], userId)):
            if settings["useCooldownMessages"]:
                if Parent.GetCooldownDuration(ScriptName, settings["command"]) > Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId):
                    cd = Parent.GetCooldownDuration(ScriptName, settings["command"])
                    outputMessage = settings["onCooldown"]
                else:
                    cd = Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId)
                    outputMessage = settings["onUserCooldown"]
                outputMessage = outputMessage.replace("$cd", str(cd))
            else:
                outputMessage = ""
        else:
            outputMessage = generate(username)
            if settings["useCooldown"]:
                Parent.AddUserCooldown(ScriptName, settings["command"], userId, settings["userCooldown"])
                Parent.AddCooldown(ScriptName, settings["command"], settings["cooldown"])

        outputMessage = outputMessage.replace("$user", username)
        outputMessage = outputMessage.replace("$command", settings["command"])
        Parent.SendStreamMessage(outputMessage)
    return


def ReloadSettings(jsonData):
    Init()

    return


def Tick():
    return
