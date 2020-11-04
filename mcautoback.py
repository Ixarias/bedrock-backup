import ctypes, sys
import shutil
import os
from os import path
from datetime import datetime
from time import sleep
from glob import glob
from dearpygui import core, simple
from dearpygui.core import add_text, get_value, log_debug, run_async_function, start_dearpygui
from dearpygui.simple import show_about, show_documentation

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def bedrockpathtostr(worldname):
    worldpath = path.expandvars('%localappdata%/Packages/Microsoft.MinecraftUWP_8wekyb3d8bbwe/LocalState/games/com.mojang/minecraftWorlds')

    result = [y for x in os.walk(worldpath) for y in glob(os.path.join(x[0], '*.txt'))]
    for x in result:
        txtfile = open(x)
        if txtfile.readline() == worldname:
            return x[:-13]
    
    return('Not Found')

def findworld(worldname):
    bedrockpath = bedrockpathtostr(worldname)
    if bedrockpath == 'Not Found':
        log_debug(bedrockpath)
        return(0)
    backuppath = path.expandvars('%localappdata%/Packages/Microsoft.MinecraftUWP_8wekyb3d8bbwe/LocalState/games/com.mojang/minecraftWorlds/' + worldname + "_")
    bedrockname = bedrockpath[119:]
    return backuppath, bedrockpath, bedrockname

def dobackup(backuppath, bedrockpath, WaitTime, FailMod):
    while True:
        try:
            fullpath = backuppath + str(datetime.now().strftime('[%Y_%m_%d]_[%H_%M]'))
            shutil.make_archive(fullpath, 'zip', bedrockpath)
            # log_debug(f"New Backup made at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            # log_debug('Waiting ' + str(WaitTime) + ' seconds')
            sleep(WaitTime)
        except KeyboardInterrupt:
            sys.exit()
        except:
            # log_debug('Backup unavailable while the Minecraft World is running')
            # log_debug('Trying again in ' + str(WaitTime/FailMod) + ' seconds')
            sleep(FailMod)

def backupprep(sender, data):
    backupinfo = (get_value("World Name"), get_value("Wait Time"), get_value("Failure Wait Time"))
    add_text(f"Backup created at {datetime.now().strftime('[%Y_%m_%d]_[%H_%M]')}", parent="MCAutoBack")
    run_async_function(backupcallback, backupinfo, return_handler=backupprep)

def backupcallback(sender, data):
    worldinfo = findworld(data[0])
    dobackup(worldinfo[0], worldinfo[1], data[1], data[2])

if __name__ == '__main__':
    core.set_main_window_size(600, 200)

    with simple.window("MCAutoBack"):
        core.add_text("MCAutoBack")
        core.add_input_text("World Name", default_value="Cube World")
        core.add_button("Backup", callback=backupprep)
        core.add_slider_int("Wait Time", default_value=300, min_value=30, max_value=1200)
        core.add_slider_int("Failure Wait Time", default_value=30, min_value=5, max_value=300)

    start_dearpygui(primary_window="MCAutoBack")