import os
import time
import datetime
import json
import logging
import sys


def timenow():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

def convert_back_to_date_time(strftime: str):
    return datetime.datetime.strptime(strftime, "%Y-%m-%d %H:%M:%S")

def update_last_shutdown():
    with open("last_shutdown.date", "w") as fp:
        fp.write(timenow())

def get_last_shutdown():
    with open("last_shutdown.date", "r") as fp:
        return convert_back_to_date_time(fp.read())

def shutdowned_today():
    try:
        last_shutdown = get_last_shutdown()
    except FileNotFoundError:
        return False
    return datetime.datetime.now().date() == last_shutdown.date()



ARBITRARY_DATE = datetime.datetime(1988, 3, 14)
def is_time_between(t, start, end): # https://github.com/allan-silva/py-time-between
    if start == end:
        return True
    day_add = 1 if end < start else 0
    end_add = 1 if day_add and end == datetime.time(0,0,0,0) else 0
    test_add = 1 if day_add and t < start else 0
    td_time_start = datetime.timedelta(hours=start.hour,
                              minutes=start.minute,
                              seconds=start.second,
                              microseconds=start.microsecond)
    td_time_end = datetime.timedelta(days=day_add + end_add,
                            hours=end.hour,
                            minutes=end.minute,
                            seconds=end.second,
                            microseconds=end.microsecond)
    td_testing = datetime.timedelta(days=test_add,
                           hours=t.hour,
                           minutes=t.minute,
                           seconds=t.second,
                           microseconds=t.microsecond)
    start_date = ARBITRARY_DATE + td_time_start
    end_date = ARBITRARY_DATE + td_time_end
    testing_date = ARBITRARY_DATE + td_testing
    return start_date <= testing_date and testing_date <= end_date


def get_name_of_day():
    now = datetime.datetime.now()
    return now.strftime("%A")


def simple_is_time_between(start: str, end: str) -> bool:
    start = start.split(':')
    start = datetime.time(int(start[0]), int(start[1]))
    end = end.split(':')
    end = datetime.time(int(end[0]), int(end[1]))
    
    now = time.strftime('%H:%M').split(':')
    now = datetime.time(int(now[0]), int(now[1]))
    return is_time_between(now, start, end)
    

def shutdown_pc() -> None:
    if os.name == 'posix': # Linux
        os.system('echo 1 > /proc/sys/kernel/sysrq && echo o > /proc/sysrq-trigger') # root previlegs required
    else:
        os.system('C:\\Windows\\System32\\shutdown.exe -s -t 0')
    update_last_shutdown()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    with open("config.json", "r") as fp:
        config = json.load(fp)

    STRICT_MODE = config['strict_mode']

    if config['enabled']:
        while True:
            if not STRICT_MODE and shutdowned_today():
                logging.debug("Already shutdowned today, skipping...")
            else:
                if config['days']['every_day']['from']:
                    day = 'every_day'
                else:
                    day = get_name_of_day()

                if config['days'][day]['from']:
                    if simple_is_time_between(config['days'][day]['from'], config['days'][day]['to']):
                        logging.info("Shutting down..")
                        shutdown_pc()
                    else:
                        logging.debug("Time isn't between")
                else:
                    logging.debug("Time is none, skipping...")
            time.sleep(15)
    else:
        logging.info("Not enabled. exiting...")