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
            pass

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
