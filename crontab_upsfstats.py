# -*- coding: utf-8 -*-
import sys
import voltage_recorder

# Configuration path and filename
config_path = "config.json"
# CGI prograam, upsfstats URL:
upsfstats = "http://192.168.0.1/upsfstats.cgi?host=127.0.0.1"

# Raw filter configuration is needed
result = voltage_recorder.apcupsd_upsfstats(upsfstats, config_path)
if type(result) is list:
    print(result[1])
else:
    pass

sys.exit(0)
