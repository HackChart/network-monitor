import subprocess
import json
import logging
import os
import csv
from time import sleep
from sys import exit


# TODO: [] CONVERT BYTE DATA TO HUMAN READABLE FORM FOR EXPORT
# TODO: [] CHECK FOR RETURN CODE IF SUCCESSFUL RUN
# TODO: [] IMPLEMENT LOGGING WHERE APPLICABLE
# TODO: [] WRITE A README
# TODO: [] CLEANUP 
# ----- PROOF OF CONCEPT ----- #
# designed to monitor network performance by automating tests
class Speedtest:
    def __init__(self):
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
                    for key, value in config_data.items():
                        if key in ['wait', 'retries']:
                            try:
                                int(value)
                            except TypeError as e:
                                # TODO: LOG E
                                exit(2)
                        else:   # assumes all other config entries should be paths
                            try:
                                str(value)
                            except TypeError as e:
                                # TODO: LOG E
                                exit(2)
                        setattr(self, key, value)
        else:
            # TODO: FAILURE TO FIND CONFIG FILE
            # TODO: RAISE CUSTOM ERR, LOG, EXIT
            pass

        try:
            results = subprocess.check_output([getattr(self, 'cli_path'), '-f', 'json'])
        except FileNotFoundError as err:
            # TODO: CHANGE TO LOGGING LATER, EXIT
            print(f'FileNotFound: {err}]')
        except subprocess.CalledProcessError as e:
            # TODO: LOG FAILURE, WAIT, TRY AGAIN
            for _ in getattr(self, "retries"):
                # TODO: LOG - TRYING N OF X
                sleep(getattr(self, "wait"))
                # TODO: CHECK FOR RETURN CODE FOR BREAK
                retry = Speedtest()   # run another test
                if len(vars(retry)) > 10:   # check whether results were appended
                    retry.to_csv()
                    # TODO: LOG SUCCESS OF N
                    exit(0)
            # TODO: LOG RETRY FAILURE
            exit(2)
        else:
            # dynamically set result obj attributes
            jdata = json.loads(results)   # convert results to json
            self.set_attributes(jdata)
        # TODO: LOG SUCCESS / FAILURE

    def set_attributes(self, data):
        """Sets obj attributes from json"""
        for key, value in data.items():
            if type(value) is not dict:
                setattr(self, key, value)
            else:
                for nested_key, nested_value in data[key].items():
                    setattr(self, f'{key}_{nested_key}', nested_value)
                    # create human-readable entries for network speed
                    if 'bandwidth' in nested_key:
                        setattr(
                            self,
                            f'{key}_{nested_key}_Mbps',
                            round(nested_value / 125_000, 2
                                  ))
        # checks to see if packetLoss needs to be set
        if getattr(self, "packetLoss", None) is None:
            setattr(self, "packetLoss", "N/A")

    def to_csv(self):
        # REMOVE CONFIG ATTRS FROM ATTRS TO APPEND
        config_attrs = ['cli_path', 'log_path', 'output', 'retries', 'wait']
        csv_data = {key: value for key, value in vars(self).items()
                    if key not in config_attrs}
        # write to file
        if not os.path.exists(getattr(self, "output")):
            # if no file, create header
            with open(getattr(self, "output"), 'w') as f:
                writer = csv.DictWriter(f, fieldnames=list(csv_data.keys()))
                writer.writeheader()
                # TODO: LOG NEW FILE CREATED AT PATH
        # append result data
        with open(getattr(self, "output"), 'a') as f:
            writer = csv.DictWriter(f, fieldnames=list(csv_data.keys()))
            writer.writerow(csv_data)
            # TODO: LOG FILE APPENDED PROPERLY


# TODO: REMOVE LATER, JUST FOR TESTING
if __name__ == '__main__':
    for i in range(2):
        x = Speedtest()
        print(len(vars(x)), vars(x))
        x.to_csv()