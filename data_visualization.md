
### Data preprocessing
Convert recording file.
```python
# -*- coding: utf-8 -*-
import pandas

# Read csv file
voltage_record_file = pandas.read_csv( "apcupsd_voltage_record.csv", sep=",", header=None )
# Define columns name
voltage_dataframe = pandas.DataFrame(voltage_record_file.values, columns = ["Datetime", "Voltage", "Source"])
# Define Datetime
voltage_dataframe["Datetime"] = pandas.to_datetime(voltage_dataframe["Datetime"], format="%Y-%m-%d %H:%M:%S%z")
voltage_dataframe["Voltage"] = voltage_dataframe["Voltage"].map(lambda x: x.rstrip("Volts"))
# Split into date and time
voltage_dataframe["Date"] = pandas.to_datetime(voltage_dataframe["Datetime"]).dt.date
voltage_dataframe["Time"] = pandas.to_datetime(voltage_dataframe["Datetime"]).dt.time
# Rearrangements
voltage_dataframe = voltage_dataframe[["Datetime", "Date", "Time", "Voltage", "Source"]]
# Drop it
voltage_dataframe = voltage_dataframe.drop(columns=["Datetime", "Source"])
# Save to csv
voltage_dataframe.to_csv( "voltage_graphic.csv", sep=",", header=None, index=None )

```

### Using Matplotlib plot data
```python
# -*- coding: utf-8 -*-
import pandas
import matplotlib.pyplot as graphic

daily_voltages = [
    "2022-07-25.csv",
    "2022-07-26.csv",
    "2022-07-27.csv",
    "2022-07-28.csv",
    "2022-07-29.csv",
    "2022-07-30.csv",
    "2022-07-31.csv"
    ]

for daily_voltage in daily_voltages:
    voltage_24 = pandas.read_csv( daily_voltage, sep=",", header=None )
    voltage_24 = pandas.DataFrame( voltage_24.values, columns = ["Date", "Time", "Voltage"] )
    graphic.plot(voltage_24.Time, voltage_24.Voltage, linewidth=5, color="r")
    # Image size
    graphic.rcParams["figure.figsize"] = [48, 30]
    graphic.xticks( voltage_24.Time, rotation=-75, fontsize=20 )
    graphic.yticks( fontsize=30 )
    # Voltge range, base on your country standard voltage
    graphic.ylim( 106, 116 )
    # Title
    graphic_title = daily_voltage.replace( ".csv"," Daily Voltage Record" )
    graphic.title( graphic_title, fontsize=60 )
    # Enable grid
    graphic.grid( True )
    # File name
    imagename = daily_voltage.replace( "csv","png" )
    # Save into image file
    graphic.savefig( "graphic"+" "+imagename )
    # Clean graphic function cache
    # HIGHLY NECESSARY !!!! OTHERWISE THE IMAGE WILL OVERLAPPING !!!
    graphic.clf()
```