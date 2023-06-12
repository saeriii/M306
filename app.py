import os
import xml.etree.ElementTree as ET
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/zaehlerstaende')
def zaehlerstaende():
    tag_values = read_esl_files()
    test = "tests"
    return render_template('zaehlerstaende.html', values=tag_values, test=test)


def read_esl_files():
    count = 0
    tag_values = {}
    folder_path = "C:/Users/Saranya Wenger/PycharmProjects/M306/files/ESL-Files"
    bezug = ["1-1:1.8.1", "1-1:1.8.2"]
    for file_name in os.listdir(folder_path):  # loop through all files
        if file_name.endswith(".xml"):
            file_path = os.path.join(folder_path, file_name)
            file_data = []
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                for value_row in root.findall(".//ValueRow"):  # through all rows
                    obis = value_row.attrib.get("obis")
                    if obis in bezug:
                        data = {}
                        tag_value = float(value_row.attrib.get("value"))
                        data['timestamp'] = value_row.attrib.get("valueTimeStamp", None)
                        if count == 0:
                            value1 = tag_value
                            count += 1
                        else:
                            tag_value = value1 + tag_value
                            data['value'].append(tag_value)
                            count = 0
            except ET.ParseError:
                print(f"Error parsing XML file: {file_path}")

    return data


if __name__ == '__main__':
    app.run()
