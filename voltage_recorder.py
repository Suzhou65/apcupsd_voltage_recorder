# -*- coding: utf-8 -*-
import csv
import json
import requests
import subprocess
from bs4 import BeautifulSoup

# Configuration function
def configuration(config_path=()):
    # Load configuration by parameter or using default
    if bool(config_path) is False:
        # Default configuration filename and path
        config_path = "config.json"
    elif bool(config_path) is True:
        pass
    # Load configuration
    try:
        with open(config_path, "r") as configuration_file:
            #Return dictionary
            return json.load(configuration_file)
    # If configuration not found
    except FileNotFoundError:
        #Initialization
        print("Configuration not found, please initialize.\r\n")
        input_schedule_minutes = input("Please enter schedule time, in minutes: ")
        input_recordpath = input("Please enter recording filename: ")
        input_raw_date = input("Please enter row number of DATE: ")
        input_raw_voltage = input("Please enter row number of LINEV: ")
        #Check filename extension
        extension = ".csv"
        if extension in input_recordpath:
            recording_path = input_recordpath
        else:
            recording_path = input_recordpath + extension
        #Dictionary
        initialize_config = {
            "schedule_config": input_schedule_minutes,
            "record_path": recording_path,
            "raw_date": input_raw_date,
            "raw_voltage": input_raw_voltage,
            "prefix_date": "",
            "prefix_voltage": ""
            }
        #Save configuration file
        with open(config_path, "w") as configuration_file:
            json.dump(initialize_config, configuration_file, indent=2)
            print("Configuration saved successfully.")
            #Return dictionary after initialize
            return initialize_config

#Asking apcaccess
def apcupsd_apcaccess(config_path=(), separate=()):
    #Load config
    load_config = configuration(config_path)
    #Saving filename
    recording_file = load_config["record_path"]
    #Row numbers of data
    date_row = load_config["row_date"]
    voltage_row = load_config["row_voltage"]
    #Remove prefix
    date_prefix = load_config["prefix_date"]
    line_prefix = load_config["prefix_voltage"]
    #Ask voltage data and save
    apcaccess_bytes = subprocess.run(["apcaccess"], stdout=subprocess.PIPE)
    apcaccess_srting = apcaccess_bytes.stdout.decode('utf-8')
    apcaccess_list = apcaccess_srting.split("\n")
    #Using parameters input as Need row numbers
    if type(separate) is list:
        separate_date = separate[0]
        separate_voltage = separate[1]
        recording_data = [apcaccess_list[separate_date].replace(date_prefix, ""), apcaccess_list[separate_voltage].replace(line_prefix, ""), "apcaccess"]
        with open(recording_file, mode="a", newline="") as tape:
            recording=csv.writer(tape)
            recording.writerow(recording_data)
            tape.close()
        return recording_data
    #Using configuration setting as row numbers
    elif bool(separate) is False:
        recording_data = [apcaccess_list[date_row].replace(date_prefix, ""), apcaccess_list[voltage_row].replace(line_prefix, ""), "apcaccess"]
        with open(recording_file, mode="a", newline="") as tape:
            recording=csv.writer(tape)
            recording.writerow(recording_data)
            tape.close()
        return recording_data

#Asking upsfstats.cgi
def apcupsd_upsfstats(upsfstats, config_path=(), separate=()):
    #Load config
    load_config = configuration(config_path)
    #Saving filename
    recording_file = load_config["record_path"]
    #Row numbers of data
    date_row = load_config["row_date"]
    voltage_row = load_config["row_voltage"]
    #Remove prefix
    date_prefix = load_config["prefix_date"]
    line_prefix = load_config["prefix_voltage"]
    #Need upsfstats.cgi adrss
    if bool(upsfstats) is False:
        error_message = ["Error", "Address of upsfstats.cgi is necessary"]
        with open(recording_file, mode="a", newline="") as tape:
            recording=csv.writer(tape)
            recording.writerow(error_message)
            tape.close()
        return False
    elif bool(upsfstats) is True:
        #Access apcupsd
        try:
            apcupsd_respon = requests.get(upsfstats, timeout=5)
            if apcupsd_respon.status_code == 200:
                html_content = apcupsd_respon.content
                apcupsd_respon.close()
                #Using BeautifulSoup
                batterysoup = BeautifulSoup(html_content,"html.parser")
                dataframe = batterysoup.find("pre").text
                data_output = dataframe.split("\n")
                #Using parameters input as row numbers
                if type(separate) is list:
                    separate_date = separate[0]
                    separate_voltage = separate[1]
                    recording_data = [data_output[separate_date].replace(date_prefix, ""), data_output[separate_voltage].replace(line_prefix, ""), "upsfstats"]
                    #Saveing
                    with open(recording_file, mode="a", newline="") as tape:
                        recording=csv.writer(tape)
                        recording.writerow(recording_data)
                        tape.close()
                    return recording_data
                #Using configuration setting as row numbers
                elif bool(separate) is False:
                    recording_data = [data_output[date_row].replace(date_prefix, ""), data_output[voltage_row].replace(line_prefix, ""), "upsfstats"]
                    #Saveing
                    with open(recording_file, mode="a", newline="") as tape:
                        recording=csv.writer(tape)
                        recording.writerow(recording_data)
                        tape.close()
                    return recording_data
        #Timeout error
        except requests.exceptions.Timeout:
            return 504
        #Error
        except Exception:
            return True
