import json,os,psutil,datetime,subprocess,signal,threading
from time import sleep

f = open("config.json",'r+')
config = json.load(f)
Max_Ram = config['max_ram']
Server_Path = config['Path_To_Server']
Max_System_Ram = config['max_system_ram']
failed_scan = False
high_priority = config['high_priority']

def logging(content):
    logfile = open('server_perf_log.txt','a')
    logfile.write(str(datetime.datetime.now())+'|'+ content + '\n')
    print(str(datetime.datetime.now())+'|'+ content)
    logfile.close()

def checkram():
    global failed_scan
    try:
        failed_scan = False
        mem_per = 0
        #Attempt at detecting application memory usage
        for process in psutil.process_iter():
            if 'deadmatterServer-Win64-Test' in str(process):
                pid = process.pid
                name = process.name()
                mem_per = round(psutil.Process(pid).memory_percent(),2)
                break
        #Fallback method incase python gets denied application memory usage
        if mem_per == 0:
            pid = "Using System Ram"
            name = "Failed to scan server. Using Fallback"
            mem_per = psutil.virtual_memory().percent
            #Sets failed scan to true to notify other fucntions
            failed_scan = True
        return mem_per,pid,name
    except:
        mem_per = 0
        pid = 'connection error'
        name = 'connection error'   
        if mem_per == int:
            pass
        else:
            pass
        return mem_per,pid,name

def check_restart():
    print('Started Up Memory Check Module')
    while 1:
        try:
            current_mem = checkram()[0]
            if current_mem > Max_Ram and failed_scan == False:
                logging(f'Max Ram Met. Current Ram:{current_mem}% Server Restarting.')
                os.system("TASKKILL /F /IM deadmatterServer-Win64-Test.exe")
                sleep(5)
            elif failed_scan == True:
                if current_mem > Max_System_Ram and failed_scan == True:
                    logging(f'Max System Ram Met. Current Ram:{current_mem}% Server Restarting.')
                    os.system("TASKKILL /F /IM deadmatterServer-Win64-Test.exe")
                    sleep(5)
        except:
            sleep(5)
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
    print('Started Up Auto Restart Module')
    while 1:
        if checkram()[0] < Max_Ram and process_exists('deadmatterServer.exe') == False:
            logging('Server not found. Starting Server.')
            subprocess.Popen([Server_Path, "-log"])
        elif process_exists('deadmatterServer.exe') == True and checkram()[0] < Max_Ram:
            if failed_scan == False:
                logging(f'Monitoring:{checkram()[2]} | PID:{checkram()[1]} | Current Ram Usage:{checkram()[0]}% | Max Ram Usage:{Max_Ram}%')
            elif failed_scan == True:
                logging(f'USING FALLBACK|Monitoring:{checkram()[2]} | PID:{checkram()[1]} | Current System Ram Usage:{checkram()[0]}% | Max Ram Usage:{Max_Ram}%')
        sleep(5)

def Ram_Cleaner():
    print('Started Up Ram Cleaning Module')
    while 1:
        try:
            os.startfile('RamCleaner.bat')
            logging('Cleaned Ram')
            sleep(60)
        except:
            logging('Error Cleaning Ram')

#Checks if process has High Priority or not
def High_Priority():
    if high_priority == True:
        print('Started Up High Priority Module')
    while 1:
        try:
            if high_priority == True and process_exists('deadmatterServer.exe') == True:
                while 1:
                    for process in psutil.process_iter():
                        if 'deadmatterServer-Win64-Test' in str(process):
                            p = psutil.Process(os.getpid())
                            if 'HIGH_PRIORITY_CLASS' in str(p.nice()):
                                pass
                            else:
                                p.nice(psutil.HIGH_PRIORITY_CLASS)
                            break
                        else:
                            pass
                    sleep(60)
            else:
                pass
        except Exception as ex:
            print(f'Coudnt set High Prio Error:{str(ex)}')
            pass

if __name__ == "__main__":
    try:
        threading.Thread(target=check_restart).start()
        threading.Thread(target=Auto_Restart).start()
        threading.Thread(target=Ram_Cleaner).start()
        if high_priority == True:
            threading.Thread(target=High_Priority).start()
    except:
        print('Failure during startup. Please try again')
        quit()
    print('Monitoring Started.')
