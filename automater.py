import subprocess
import json
import logging
import os


# ----- PROOF OF CONCEPT ----- #
# designed to monitor network performance by automating tests
class Speedtest:
    def __init__(self):
        # capture result data from CLI utility
        # TODO: SEARCH FOR CONFIG FILE
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

        try:
            # TODO: CHECK CONFIG FILE FOR CLU PATH
            results = subprocess.check_output(['./speedtest', '-f', 'json'])
        except FileNotFoundError as err:
            # TODO: CHANGE TO LOGGING LATER
            print(f'FileNotFound: {err}]')
        else:
            # dynamically set result obj attributes
            jdata = json.loads(results)   # convert results to json
            self.set_attributes(jdata)   #
        # TODO: LOG SUCCESS / FAILURE
        # TODO: CHECK CONFIG FILE FOR OUTPUT FILE
        # TODO: APPEND RESULTS

    def set_attributes(self, data):
        """Sets obj attributes from json"""
        for key in data:
            if type(data[key]) != dict:
                setattr(self, key, data[key])
            else:
                for nested_key, value in data[key].items():
                    setattr(self, f'{key}_{nested_key}', value)
