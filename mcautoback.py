import ctypes, sys
import shutil
import os
from os import path
from datetime import datetime
from time import sleep
from glob import glob
from dearpygui import core, simple
from dearpygui.core import add_text, get_value, log_debug, run_async_function, show_logger, start_dearpygui
from dearpygui.simple import show_about, show_debug, show_documentation

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

def dobackup(backuppath, bedrockpath):
        try:
            fullpath = backuppath + str(datetime.now().strftime('[%Y_%m_%d]_[%H_%M]'))
            shutil.make_archive(fullpath, 'zip', bedrockpath)
            os.rename(fullpath + '.zip', fullpath + '.mcworld')
            log_debug(f"New Backup made at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            return 1
        except KeyboardInterrupt:
            return 0
        except:
            return 0

def async_sleep(sender, sleeptime):
    sleep(sleeptime)

def backupcallback(sender, data):
    backupinfo = (get_value("World Name"), get_value("Wait Time"), get_value("Failure Wait Time"))
    worldinfo = findworld(backupinfo[0])
    if (dobackup(worldinfo[0], worldinfo[1]) == 1):
        add_text(f"Backup created at {datetime.now().strftime('[%Y_%m_%d]_[%H_%M]')}", parent="MCAutoBack")
        run_async_function(async_sleep, backupinfo[1], return_handler=backupcallback)
    else:
        add_text(f'Backup failed. Is the world being accessed?', parent="MCAutoBack")
        run_async_function(async_sleep, backupinfo[2], return_handler=backupcallback)
    
if __name__ == '__main__':
    core.set_main_window_size(600, 200)

    with simple.window("MCAutoBack"):
        core.add_text("MCAutoBack")
        core.add_input_text("World Name", default_value="Cube World")
        core.add_button("Backup", callback=backupcallback)
        core.add_slider_int("Wait Time", default_value=300, min_value=30, max_value=1200)
        core.add_slider_int("Failure Wait Time", default_value=30, min_value=5, max_value=300)

    show_logger()
    start_dearpygui(primary_window="MCAutoBack")