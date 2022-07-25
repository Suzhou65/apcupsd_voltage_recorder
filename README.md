# Apcupsd Voltage Recorder
[![python version](https://github.takahashi65.info/lib_badge/python-3.6.svg)](https://www.python.org/) 
[![UA](https://github.takahashi65.info/lib_badge/active_maintenance.svg)](https://github.com/Suzhou65/apcupsd_voltage_recorder)
[![Size](https://github-size-badge.herokuapp.com/Suzhou65/apcupsd_voltage_recorder.svg)](https://github.com/axetroy/github-size-badge)

Recording utility power voltages from apcupsd.

## Contents
- [Apcupsd Voltage Recorder](#apcupsd-voltage-recorder)
  * [Contents](#contents)
  * [Usage](#usage)
    + [Scheduling](#scheduling)
    + [Configuration](#configuration)
    + [Cron mode](#cron-mode)
    + [Schedule mode](#schedule-mode)
 * [Dependencies](#dependencies)
    + [Python version](#python-version)
    + [Python module](#python-module)

## Usage
### Scheduling
Using schedule module for job scheduling, you can found the scheduling setting at configuration file.

Alternative solution is using Linux built-in ```Cron``` function.
### Configuration
Store configuration as JSON format file, named config.json.

You can editing the clean copy, which looks like this:
```json
{
  "schedule_config": 10,
  "path_and_filename": "apcupsd_voltage_record.csv",
  "row_date": 1,
  "row_voltage": 11,
  "prefix_date":"",
  "prefix_voltage":""
}
```
- ```schedule_config``` setting the execution period.
- ```path_and_filename``` setting the voltage recording filename and storage path.
- ```row_date``` reference to row number of datetime.
- ```row_voltage``` reference to row number of voltage report.
- ```prefix_date``` delete the prefix at datetime row.
- ```prefix_voltage``` delete the prefix at voltage row.

### Cron mode
Startup script by Linux built-in ```Cron``` function.
- Get voltage data from apcaccess
```shell
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
0 */1   * * *   pi python /python_script/crontab_apcaccess.py
#
```
- Get voltage data from apcupsd-cgi program
```shell
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
0 */1   * * *   pi python /python_script/crontab_upsfstats.py
#
```
### Schedule mode
- Get voltage data from apcaccess
```
user@localhost:~/python_script python schedule_apcaccess.py
```
- Get voltage data from apcupsd-cgi program
```
user@localhost:~/python_script python schedule_upsfstats.py
```
After startup, it will print this:
```
Scheduled period is 10 minutes.
Pressing CTRL+C to exit voltage monitor.
```
If you want to terminate the Program, pressing CTRL+C, it will print this:
```
^C
Thank you for using the voltage monitor.
GoodBye ...
```

## Dependencies
### Python version
- Python 3.6 or above
### Python module
- sys
- csv
- time
- json
- schedule
- requests
- subprocess
- BeautifulSoup