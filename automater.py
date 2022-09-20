import subprocess
import json
import logging
import os
import csv


# ----- PROOF OF CONCEPT ----- #
# designed to monitor network performance by automating tests
class Speedtest:
    def __init__(self):
        # TODO: SEARCH FOR CONFIG FILE
        # CHECK CONFIG, LOAD IF EXISTS
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                try:
                    config_data = json.load(f)
                except TypeError as err:
                    # TODO: LOG ERR
                    pass
                else:
                    # SET CONFIG ATTRS
                    self.path = config_data['path']
                    self.output_file = config_data['output']
        else:
            # TODO: RAISE CUSTOM ERR, LOG, EXIT

            # TODO: LOOK INTO MERGING THIS WITH TRY BLOCK ABOVE
            pass
        try:
            results = subprocess.check_output([self.path, '-f', 'json'])
        except FileNotFoundError as err:
            # TODO: CHANGE TO LOGGING LATER
            print(f'FileNotFound: {err}]')
        else:
            # dynamically set result obj attributes
            jdata = json.loads(results)   # convert results to json
            self.set_attributes(jdata)   #
        # TODO: LOG SUCCESS / FAILURE

    def set_attributes(self, data):
        """Sets obj attributes from json"""
        for key in data:
            if type(data[key]) != dict:
                setattr(self, key, data[key])
            else:
                for nested_key, value in data[key].items():
                    setattr(self, f'{key}_{nested_key}', value)

    def to_csv(self):
        # REMOVE NON RELEVANT ATTRS FROM ATTRS TO APPEND
        csv_data = {key: value for key, value in vars(self).items() if key != 'path' and key != 'output_file'}
        # write to file
        # TODO: FIX - ROWS ARE MISMATCHED FROM TIME TO TIME, POTENTIALLY NOT APPENDING FOR NULL VALUE?
        if not os.path.exists(self.output_file):
            # if no file, create header
            with open(self.output_file, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=list(csv_data.keys()))
                writer.writeheader()
        # append result data
        with open(self.output_file, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=list(csv_data.keys()))
            writer.writerow(csv_data)

        # TODO: PROBABLY A DIFFERENT OBJ, BUT IMPLEMENT GRAPHING AND BYTE CONVERSION
        # TODO: FOR READABILITY

        # TODO: TRY TO BREAK ALL OF THIS


if __name__ == '__main__':
    for i in range(2):
        x = Speedtest()
        print(len(vars(x)), vars(x))
        x.to_csv()