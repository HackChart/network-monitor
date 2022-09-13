import subprocess
import json
import logging
from server import Server
from connection import Connection


# ----- PROOF OF CONCEPT ----- #
# designed to monitor network performance by automating tests
class Speedtest:
    def __init__(self):
        # capture result data from CLI utility
        # TODO: HANDLE CLI PATH EXECUTION
        results = subprocess.check_output(['./speedtest', '-f', 'json'])
        jdata = json.loads(results)   # convert results to json
        # TODO: LOG SUCCESS / FAILURE
        # TODO: CHECK IF NETWORK DATABASE EXISTS, IF NOT, CREATE
        # TODO: APPEND RESULTS
        # TODO: CREATE RESULTS OBJECT

    def set_attributes(self, data):
        """Sets obj attributes from json"""
        for key in data:
            if type(data[key]) != dict:
                setattr(self, key, data[key])
            else:
                for nested_key, value in data[key].items():
                    setattr(self, f'{key}_{nested_key}', value)
