# -*- coding: utf-8 -*-
import sys
import voltage_recorder

# Configuration path and filename
config_path = "config.json"

# Raw filter configuration is needed
result = voltage_recorder.apcupsd_apcaccess(config_path)
if type(result) is list:
    print(result)
else:
    pass

sys.exit(0)
