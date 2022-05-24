import eel
import psutil
import json
import os
import subprocess

eel.init('web')

@eel.expose
def killProcess(processName):
    for i in range(0,4):
        if i != 3:
            for proc in psutil.process_iter():
                if proc.name() == processName:
                    proc.kill()
        else:
            alive=False
            for proc in psutil.process_iter():
                if proc.name() == processName:
                    alive=True
            if alive==False:
                return json.dumps({"status": "success", "message": "Successfully killed process"})
            else:
                return json.dumps({"status": "error", "message": "Failed to kill process"})

@eel.expose
def modifyDiscordSettings(settingsFilePath, urls):
    settings = {}
    if "%appdata%" in settingsFilePath:
        settingsFilePath = settingsFilePath.replace("%appdata%", os.getenv("APPDATA"))
    
    try:
        with open(settingsFilePath, "r") as settingsFile:
            settings = json.load(settingsFile)
    except:
        return json.dumps({"status": "error", "message": "Failed to open settings file"})

    for key, value in urls.items():
        settings[key] = value

    try:
        with open(settingsFilePath, "w") as settingsFile:
            json.dump(settings, settingsFile, indent=4, sort_keys=True)
    except:
        return json.dumps({"status": "error", "message": "Failed to write settings file"})


    return json.dumps({"status": "success", "message": "Successfully modified discord settings"})


@eel.expose
def startDiscord(updateExecutablePath, executableName):

    if "%localappdata%" in updateExecutablePath:
        updateExecutablePath = updateExecutablePath.replace("%localappdata%", os.getenv("LOCALAPPDATA"))
    
    try:
        retCode = subprocess.call([updateExecutablePath, '--processStart', executableName])
    except:
        return json.dumps({"status": "error", "message": "Failed to start Discord"})
    
    return json.dumps({"status": "success", "message": "Discord should have started"})


eel.start('index.html', size=(640, 320))