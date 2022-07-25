# -*- coding: utf-8 -*-
import sys
import time
import schedule
import voltage_recorder

# Configuration path and filename
config_path = "config.json"

# Asking schedule minutes
time_configuration = voltage_recorder.configuration(config_path)
schedule_minutes = time_configuration["schedule_config"]

# Raw filter configuration is needed
def voltage_check():
    result = voltage_recorder.apcupsd_apcaccess()
    if type(result) is list:
        print(result)
        return result
    else:
        return False

# Scheduled configuration
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
