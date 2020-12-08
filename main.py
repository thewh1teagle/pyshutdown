import datetime
import os
import configparser
import time
import datetime
import timebetween
from time import sleep





def is_time_between(start, end):
    start = start.split(':')
    start = datetime.time(int(start[0]), int(start[1]))
    end = end.split(':')
    end = datetime.time(int(end[0]), int(end[1]))
    
    now = time.strftime('%H:%M').split(':')
    now = datetime.time(int(now[0]), int(now[1]))
    return timebetween.is_time_between(now, start, end)
    


def detect_os():
    if os.name == 'posix':
        return 'linux'
    else:
        return 'windows'

def shutdown_pc():
    if detect_os() == 'windows':
        os.system('C:\\Windows\\System32\\shutdown.exe -s -f -t 0')
    else:
        os.system('sudo shutdown now') 



if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    enabled = config['shutdown']['enabled']
    start_time = config['shutdown']['from']
    end_time = config['shutdown']['to']
    if is_time_between(start_time, end_time):
        print('shutting down')
        shutdown_pc()
    else:
        print("time not between")
    while True:
        if is_time_between(start_time, end_time):
            shutdown_pc()
        sleep(15)

