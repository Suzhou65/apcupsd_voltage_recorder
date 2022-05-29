# -*- coding: utf-8 -*-
import sys
import time
import schedule
import voltage_recorder

#CGI prograam, upsfstats URL:
url = "http://192.168.0.1/upsfstats.cgi?host=127.0.0.1"

#Raw filter configuration is needed
def voltage_check(upsfstats=url, date_raw=1, voltage_raw=11):
    result = voltage_recorder.apcupsd_upsfstats(upsfstats, date_raw, voltage_raw)
    if type(result) is list:
        print(result[1])
        return result
    else:
        return False

#Asking schedule minutes
time_configuration = voltage_recorder.configuration()
schedule_minutes = time_configuration["schedule_config"]
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
