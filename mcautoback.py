import ctypes, sys
import shutil
import os
from os import path
from datetime import datetime
from time import sleep
from glob import glob

#// Define time between backups, in seconds (Default: 300)
WaitTime = 300
#// Reduces wait time in case of backup failure by a factor of FailMod (Default: 5)
FailMod = 5
#// Wether to require admin permissions
RunAsAdmin = 0

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def bedrockpathtostring(worldname):
    worldpath = path.expandvars('%localappdata%/Packages/Microsoft.MinecraftUWP_8wekyb3d8bbwe/LocalState/games/com.mojang/minecraftWorlds')

    result = [y for x in os.walk(worldpath) for y in glob(os.path.join(x[0], '*.txt'))]
    for x in result:
        txtfile = open(x)
        if txtfile.readline() == worldname:
            return x[:-13]
    
def backup():

    worldname = input('Please enter world name: ')
    bedrockpath = bedrockpathtostring(worldname)
    backuppath = path.expandvars('%localappdata%/Packages/Microsoft.MinecraftUWP_8wekyb3d8bbwe/LocalState/games/com.mojang/minecraftWorlds/' + worldname + "_" + datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
    bedrockname = bedrockpath[119:]

    print(f'Backing up world folder: {bedrockname} ({worldname})')

    while True:
        try:
            shutil.make_archive(backuppath, 'zip', bedrockpath)
            print(f"New Backup made at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print('Waiting' + str(WaitTime) + seconds)
            sleep(WaitTime)
        except:
            print('Backup unavailable while the Minecraft World is running')
            print('Trying again in ' + str(WaitTime/FailMod) + ' seconds')
            sleep(WaitTime/FailMod)
        
if __name__ == '__main__':
    if RunAsAdmin == 1 and not is_admin():
        #re-run as admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    backup()