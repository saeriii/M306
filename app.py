import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/zaehlerstaende')
def zaehlerstaende():
    values = process_xml_files("C:/Users/Saranya Wenger/PycharmProjects/M306/files/ESL-Files")
    test = "tests"
    return render_template('zaehlerstaende.html', values=values, test=test)


def process_xml_files(directory):
    # Create a dictionary to store the results
    result = defaultdict(lambda: {"Bezug": 0, "Einspeisung": 0})

    # A set to store the unique timestamps
    seen_timestamps = set()

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        # Check if the current file is an XML file
        if filename.endswith('.xml'):
            # Parse the XML file
            tree = ET.parse(os.path.join(directory, filename))
            root = tree.getroot()

            # Iterate over all 'TimePeriod' elements in the XML file
            for time_period in root.iter('TimePeriod'):
                # Get the timestamp
                timestamp = time_period.get('end')

                # Check if we have already processed this timestamp
                if timestamp in seen_timestamps:
                    continue

                # Add the timestamp to the set of seen timestamps
                seen_timestamps.add(timestamp)

                # Iterate over all 'ValueRow' elements in the 'TimePeriod'
                for value_row in time_period.iter('ValueRow'):
                    # Check the 'obis' attribute and add the value to the correct category
                    obis = value_row.get('obis')
                    value = float(value_row.get('value'))

                    if obis in ["1-1:1.8.1", "1-1:1.8.2"]:
                        result[timestamp]["Bezug"] += value
                    elif obis in ["1-1:2.8.1", "1-1:2.8.2"]:
                        result[timestamp]["Einspeisung"] += value

    # Convert the defaultdict back into a dict
    return dict(result)


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
