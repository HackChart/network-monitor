import subprocess
import json
import logging
import os
import csv
from time import sleep
from sys import exit
from err import log_error
import re

# TODO: [] WRITE A README
# TODO: [] CLEANUP 
# ----- PROOF OF CONCEPT ----- #
# designed to monitor network performance by automating tests

class Speedtest:
    def __init__(self):

        # CONFIG LOGGING
        try:
            with open('config.json', 'r') as f:
                pass
        except FileNotFoundError:
            # TODO: CREATE FALLBACK LOG, LOG INCIDENT
            pass
        else:
            # TODO: TRY TO VALIDATE LOG CONFIG OPTIONS, SET LOG / FALLBACK LOG IF NOT
            try:
                # check whether path is valid string
                # TODO: USE RE TO VALIDATE THAT PATH ENDS IN .LOG

                # TODO: VALIDATE LOG LEVEL, SET TO DEBUG IF NOT VALID

                # TODO: CHANGE THIS TO REFLECT CONFIG
                logging.basicConfig(
                    filename=init_log,
                    encoding='utf-8',
                    level=log_level,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p'
                )
                logging.info('Logging configured')

        # CHECK CONFIG, LOAD IF EXISTS
        logging.debug("Checking for config file..")
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                logging.debug('Path exists, attempting to load configurations.. ')
                try:
                    config_data = json.load(f)
                except TypeError as e:
                    # improper config, log and exit
                    log_error(e)
                else:
                    # SET CONFIG ATTRS
                    logging.debug('Config data of correct format, attempting to set attributes..')
                    for key, value in config_data.items():
                        if key in ['wait', 'retries']:
                            try:
                                int(value)
                            except TypeError as e:
                                # wait or retry is of incorrect type
                                log_error(e)
                        else:   # assumes all other config entries should be paths
                            try:
                                str(value)
                            except TypeError as e:
                                # path variables are of incorrect type
                                log_error(e)
                        setattr(self, key, value)
                    logging.debug('Config data set properly.')

                    # RECONFIGURE LOG IF NEEDED
                    # TODO: REMOVE THIS WHEN UPDATED SOLUTION WORKING
                    if not init_log == getattr(self, 'log_path') or not log_level == getattr(self, 'log_level'):
                        logging.debug(f'Reconfiguring log - Path={getattr(self, "log_path")} & Log Level={getattr(self, "log_level")}')
                        for handler in logging.root.handlers[:]:
                            logging.root.removeHandler(handler)
                        logging.basicConfig(
                            filename=getattr(self, 'log_path', 'network_monitor.log'),
                            encoding='utf-8',
                            level=getattr(logging, getattr(self, 'log_level', 'WARNING').upper()),
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p'
                        )
        else:
            # config not found
            log_error('config.json not found, ensure file is located in current directory')
            raise FileNotFoundError

        # RUN SPEEDTEST, SET ATTRS
        try:
            logging.debug('Attempting speedtest..')
            results = subprocess.check_output([getattr(self, 'cli_path'), '-f', 'json'])
        except FileNotFoundError as e:
            # file doesn't exist
            log_error(e)
        except subprocess.CalledProcessError as e:
            # no internet connection, failed to run test
            logging.error(f'No internet connection - {e}')
            # attempt to rerun test
            for attempt in getattr(self, "retries"):
                logging.debug('Attempting rerun..')
                logging.debug(f'Attempt {attempt} of {getattr(self, "retries")}.')
                sleep(getattr(self, "wait"))
                retry = Speedtest()   # run another test
                if len(vars(retry)) > 10:   # check whether results were appended
                    retry.to_csv()
                    logging.debug(f'Attempt #{attempt} successful.')
                    exit(0)
                logging.debug(f'Attempt {attempt} of {getattr(self, "retries")} failed.')
            logging.debug('Attempts expended, exiting with error code 2.')
            exit(2)
        else:
            # dynamically set result obj attributes
            jdata = json.loads(results)   # convert results to json
            self.set_attributes(jdata)
            logging.debug('Test successful, attributes set.')

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
        logging.debug('Attempting to write to CSV..')
        # REMOVE CONFIG ATTRS FROM ATTRS TO APPEND
        config_attrs = ['cli_path', 'log_path', 'log_level', 'output', 'retries', 'wait']
        csv_data = {key: value for key, value in vars(self).items()
                    if key not in config_attrs}
        # write to file
        if not os.path.exists(getattr(self, "output")):
            # if no file, create header
            with open(getattr(self, "output"), 'w') as f:
                logging.debug(f'No previous output file found, creating at location: {getattr(self, "output")}')
                writer = csv.DictWriter(f, fieldnames=list(csv_data.keys()))
                writer.writeheader()
                logging.debug('Data written successfully.')
        # append result data
        with open(getattr(self, "output"), 'a') as f:
            logging.debug('Previous output file found, appending..')
            writer = csv.DictWriter(f, fieldnames=list(csv_data.keys()))
            writer.writerow(csv_data)
            logging.debug('Append successful.')


# TODO: REMOVE LATER, JUST FOR TESTING
if __name__ == '__main__':
    for i in range(2):
        x = Speedtest()
        print(len(vars(x)), vars(x))
        x.to_csv()