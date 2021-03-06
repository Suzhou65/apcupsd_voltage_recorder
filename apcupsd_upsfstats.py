# -*- coding: utf-8 -*-
import sys
import time
import schedule
import voltage_recorder

#Asking schedule minutes
time_configuration = voltage_recorder.configuration()
schedule_minutes = time_configuration["schedule_config"]

#Raw filter configuration is needed
def voltage_check():
    result = voltage_recorder.apcupsd_upsfstats(upsfstats)
    if type(result) is list:
        print(result[1])
        return result
    else:
        return False

#CGI prograam, upsfstats URL:
upsfstats = "http://192.168.0.1/upsfstats.cgi?host=127.0.0.1"

#Scheduled configuration
schedule.every(schedule_minutes).minutes.do(voltage_check)
# Running Loop
print(f"Scheduled period is {schedule_minutes} minutes.\r\nPressing CTRL+C to exit voltage monitor.")
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except Exception as error_status:
    print(error_status)
except KeyboardInterrupt:
    print("\r\nThank you for using the voltage monitor.\r\nGoodBye ...")
    sys.exit(0)
