from time import sleep
import json
import os
import psutil
import datetime
import subprocess
import threading
import shutil
from pysteamcmdwrapper import SteamCMD, SteamCMDException
def clear(): return os.system('cls')


# This Loads the Config.json
f = open("config.json", 'r+')
config = json.load(f)
Max_Ram = config['max_ram']
Server_Path = config['Path_To_Server']
Max_System_Ram = config['max_system_ram']
Server_Folder = Server_Path.strip('deadmatterServer.exe')
SteamCMDInstall = config['Steam_CMD_Path']
RamRefresh = config['RamRefresh']
AutoUpdate = config['AutoUpdate']
Ram_Refresh_Timer = config['Ram_Clean_Timer']
Server_Check_Timer = config['Server_Check_Timer']

# Global Vars
PID = 0
NAME = ""
mem_per = 0

# Logging Function


def logging(content):
    logfile = open('server_perf_log.txt', 'a')
    logfile.write(str(datetime.datetime.now())+'|' + content + '\n')
    print(str(datetime.datetime.now())+'|' + content)
    logfile.close()

# Checks the ram. Has a Failsafe implemented


def checkram():
    global PID, NAME, mem_per
    try:
        # Attempt at detecting application memory usage
        for process in psutil.process_iter():
            if 'deadmatterServer-Win64-Test' in str(process):
                PID = process.pid
                NAME = process.name()
                mem_per = round(psutil.Process(PID).memory_percent(), 2)
                if mem_per == 0:
                    PID = 'XXXX'
                    NAME = 'Connection Error'
                    mem_per = psutil.virtual_memory().percent
                break
    except Exception as ex:
        print(str(ex))
        mem_per = 0
        PID = 'XXXX'
        NAME = 'Connection Error'

# Checks Current Ram usage to Preset Cap


def check_restart():
    global mem_per
    try:
        # Nomral Restart
        if PID != 'XXXX':
            if mem_per > Max_Ram:
                logging(
                    f'Max Ram Met. Current Ram:{mem_per}% Server Restarting.')
                mem_per = 0
                os.system("TASKKILL /F /IM deadmatterServer-Win64-Test.exe")
        # Fallback Restart
        else:
            if mem_per > Max_System_Ram:
                logging(
                    f'Max System Ram Met. Current Ram:{mem_per}% Server Restarting.')
                mem_per = 0
                os.system("TASKKILL /F /IM deadmatterServer-Win64-Test.exe")
    except:
        pass

# Checks if Server is open


def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())


def Auto_Restart():
    while 1:
        # Opens Server
        if mem_per < Max_Ram and process_exists('deadmatterServer.exe') is False and PID != 'XXXX':
            logging('Server not found. Starting Server.')
            subprocess.Popen([Server_Path, "-log"])
        # Normal Logging
        elif process_exists('deadmatterServer.exe') is True and PID != 'XXXX':
            logging(
                f'Monitoring:{NAME} | PID:{PID} | Current Ram Usage:{mem_per}% | Ram Cutoff:{Max_Ram}%')
        # Fallback logging
        elif process_exists('deadmatterServer.exe') is True and PID == 'XXXX':
            logging(
                f'USING FALLBACK|Monitoring:{NAME} | PID:{PID} | Current Ram Usage:{mem_per}% | System Ram Cutoff:{Max_System_Ram}%')
        checkram()
        check_restart()
        sleep(Server_Check_Timer)


def Ram_Cleaner():
    while 1:
        try:
            os.startfile('RamCleaner.bat')
            logging('Cleaned Ram')
            sleep(Ram_Refresh_Timer)
        except:
            logging('Error Cleaning Ram')


def steaminstall(auto_update):
    try:
        try:
            os.mkdir('steam')
        except:
            pass
        steam = SteamCMD("steam")
        steam.install()
    except SteamCMDException:
        pass
    try:
        if auto_update is False:
            dirpath = input(
                'Enter Path to Server Directory (Leave blank for config.json):')
            if dirpath == '':
                dirpath = Server_Folder
        elif auto_update is True:
            dirpath = Server_Folder
        steam.login()
        try:
            os.mkdir(dirpath + '/BACKUP_FILES')
        except:
            pass
        print('BACKING UP FILES')
        for filename in os.listdir(dirpath + 'deadmatter/Saved/Config/WindowsServer'):
            original = dirpath + 'deadmatter/Saved/Config/WindowsServer/' + filename
            copy = dirpath + '/BACKUP_FILES/' + filename
            shutil.copyfile(original, copy)
        print('Backed up config files into BACKUP_FILES folder.')
        steam.app_update(1110990, dirpath, validate=True)
        print('Installed Dead Matter Dedicated Server.')
    except Exception as ex:
        print(f'Error: {str(ex)}')
    menu()


def existingsteam(steampath):
    try:
        steam = SteamCMD(steampath)
        steam.login()
        dirpath = input(
            'Enter Path to Server Directory (Leave blank for config.json):')
        if dirpath == '':
            dirpath = Server_Folder
        try:
            os.mkdir(dirpath + '/BACKUP_FILES')
        except:
            pass
        for filename in os.listdir(dirpath + 'deadmatter/Saved/Config/WindowsServer'):
            original = dirpath + 'deadmatter/Saved/Config/WindowsServer/' + filename
            print(original)
            copy = dirpath + '/BACKUP_FILES/' + filename
            print(copy)
            shutil.copyfile(original, copy)
        steam.app_update(1110990, dirpath, validate=True)
        print('Installed Dead Matter Dedicated Server.')
    except:
        print('Error Logging in.')
    menu()

# Menu Function


def menu():
    clear()
    choice = input(
        'DeadSplatter Menu\n1)Run Monitor\n2)Update / Install Server\nPlease Choose:')
    if choice == '1':
        threading.Thread(target=Auto_Restart).start()
        checkram()
        if RamRefresh:
            threading.Thread(target=Ram_Cleaner).start()
        print('Monitoring Started.')
    elif choice == '2':
        steaminput = input(
            'SteamCMD Menu\n1)local Steamcmd Install(Will Install new if no steamcmd is installed)\n2)Existing SteamCMD Install (Must be set in config.json)\nPlease choose')
        if steaminput == '1':
            steaminstall(False)
        elif steaminput == '2':
            steamdir = SteamCMDInstall
            existingsteam(steamdir)


if __name__ == "__main__":
    try:
        if AutoUpdate is True:
            auto_prompt = input(
                'Auto Updated Enabled in config.json\nWould you like to try to update? y/n\nchoice:')
            if auto_prompt == 'y' or 'Y':
                steaminstall(True)
        menu()
    except Exception as ex:
        print(f'Failure during startup. Please try again EX:{str(ex)}')
