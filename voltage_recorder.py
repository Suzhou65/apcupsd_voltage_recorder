# -*- coding: utf-8 -*-
import os
import csv
import json
import requests
import subprocess
from bs4 import BeautifulSoup

#Configuration function
def configuration():
    try:
        with open("config.json", "r") as configuration_file:
            #Return dictionary
            return json.load(configuration_file)
    except FileNotFoundError:
        #Initialization
        print("Configuration not found, please initialize.\r\n")
        input_schedule_minutes = input("Please enter schedule time, in minutes: ")
        input_filename = input("Please enter recording filename: ")
        #Check filename extension
        extension = ".csv"
        if extension in input_filename:
            recording_filename = input_filename
        else:
            recording_filename = input_filename + extension
        #Dictionary
        initialize_config = {
            "schedule_config": input_schedule_minutes,
            "filename": recording_filename,
            "prefix_date": "",
            "prefix_voltage": ""
            }
        #Save configuration file
        with open("config.json", "w") as configuration_file:
            json.dump(initialize_config, configuration_file, indent=2)
            print("Configuration saved successfully.")
            #Return dictionary after initialize
            return initialize_config

#Asking apcaccess
def apcupsd_apcaccess(date_raw,voltage_raw):
    #Load config
    load_config = configuration()
    #Saving filename
    file_name = load_config["filename"]
    #Remove prefix
    date_prefix = load_config["prefix_date"]
    line_prefix = load_config["prefix_voltage"]
    #Need row numbers
    if bool(date_raw) is False:
        error_message = ["Error", "Parameters is necessary"]
        with open(file_name, mode="a", newline="") as tape:
            recording=csv.writer(tape)
            recording.writerow(error_message)
            tape.close()
        return None
    #Ask voltage data and save
    elif bool(date_raw) is True:
        apcaccess_bytes = subprocess.run(["apcaccess"], stdout=subprocess.PIPE)
        apcaccess_srting = apcaccess_bytes.stdout.decode('utf-8')
        apcaccess_list = apcaccess_srting.split("\n")
        recording_data = [apcaccess_list[date_raw].replace(date_prefix, ""), apcaccess_list[voltage_raw].replace(line_prefix, "")]
        with open(file_name, mode="a", newline="") as tape:
            recording=csv.writer(tape)
            recording.writerow(recording_data)
            tape.close()
        return recording_data

#Asking upsfstats.cgi
def apcupsd_upsfstats(upsfstats, date_raw,voltage_raw):
    #Load config
    load_config = configuration()
    #Saving filename
    file_name = load_config["filename"]
    #Remove prefix
    date_prefix = load_config["prefix_date"]
    line_prefix = load_config["prefix_voltage"]
    #Need upsfstats.cgi adrss
    if bool(upsfstats) is False:
        error_message = ["Error", "Parameters is necessary"]
        with open(file_name, mode="a", newline="") as tape:
            recording=csv.writer(tape)
            recording.writerow(error_message)
            tape.close()
        return None
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
                #Check time and line voltage
                data_output = dataframe.split("\n")
                recording_data = [data_output[date_raw].replace(date_prefix, ""), data_output[voltage_raw].replace(line_prefix, "")]
                #Saveing
                with open(file_name, mode="a", newline="") as tape:
                    recording=csv.writer(tape)
                    recording.writerow(recording_data)
                    tape.close()
                return recording_data
        except requests.exceptions.Timeout:
            return 504
        except Exception:
            return None
