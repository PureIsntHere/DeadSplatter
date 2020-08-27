import json,os,psutil,datetime,subprocess,signal,threading
from time import sleep

f = open("config.json",'r+')
config = json.load(f)
Max_Ram = config['max_ram']
Server_Path = config['Path_To_Server']
Max_System_Ram = config['max_system_ram']

PID = 0
NAME = ""
mem_per = 0

def logging(content):
    logfile = open('server_perf_log.txt','a')
    logfile.write(str(datetime.datetime.now())+'|'+ content + '\n')
    print(str(datetime.datetime.now())+'|'+ content)
    logfile.close()

def checkram():
    global PID , NAME , mem_per
    try:
        #Attempt at detecting application memory usage
        for process in psutil.process_iter():
            if 'deadmatterServer-Win64-Test' in str(process):
                PID = process.pid
                NAME = process.name()
                mem_per = round(psutil.Process(PID).memory_percent(),2)
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

def check_restart():
    global mem_per
    try:
        #Nomral Restart
        if PID != 'XXXX':
            if mem_per > Max_Ram:
                logging(f'Max Ram Met. Current Ram:{mem_per}% Server Restarting.')
                mem_per = 0
                os.system("TASKKILL /F /IM deadmatterServer-Win64-Test.exe")
        #Fallback Restart
        else:
            if mem_per > Max_System_Ram:
                logging(f'Max System Ram Met. Current Ram:{mem_per}% Server Restarting.')
                mem_per = 0
                os.system("TASKKILL /F /IM deadmatterServer-Win64-Test.exe")
    except:
        pass

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
        #Opens Server
        if mem_per < Max_Ram and process_exists('deadmatterServer.exe') == False and PID != 'XXXX':
            logging('Server not found. Starting Server.')
            subprocess.Popen([Server_Path, "-log"])
        #Normal Logging
        elif process_exists('deadmatterServer.exe') == True and PID != 'XXXX':
            logging(f'Monitoring:{NAME} | PID:{PID} | Current Ram Usage:{mem_per}% | Ram Cutoff:{Max_Ram}%')
        #Fallback logging
        elif process_exists('deadmatterServer.exe') == True and PID == 'XXXX':
            logging(f'USING FALLBACK|Monitoring:{NAME} | PID:{PID} | Current Ram Usage:{mem_per}% | System Ram Cutoff:{Max_System_Ram}%')
        checkram()
        check_restart()
        sleep(10)

def Ram_Cleaner():
    while 1:
        try:
            os.startfile('RamCleaner.bat')
            logging('Cleaned Ram')
            sleep(60)
        except:
            logging('Error Cleaning Ram')

if __name__ == "__main__":
    try:
        threading.Thread(target=Auto_Restart).start()
        checkram()
        threading.Thread(target=Ram_Cleaner).start()
        print('Monitoring Started.')
    except Exception as ex:
        print(f'Failure during startup. Please try again EX:{str(ex)}')
