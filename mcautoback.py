import shutil
import os
from os import path
from datetime import datetime
from time import sleep
from glob import glob

#// Define time between backups, in seconds
WaitTime = 300

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
        shutil.make_archive(backuppath, 'zip', bedrockpath)
        print(f"New Backup made at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Waiting...")
        sleep(WaitTime)
        
if __name__ == '__main__':
    backup()