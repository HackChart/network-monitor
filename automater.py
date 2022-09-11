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


        # TODO: MAP OUT HOW DATA SHOULD BE STRUCTURED IN END RESULT
        # INIT ATTRS
        self.server = Server()
        self.connection = Connection()

        # results attrs
        self.timestamp = jdata["timestamp"]
        # server attrs
        self.server.id = jdata['server']['id']
        self.server.name = jdata['server']['name']
        self.server.location = jdata['server']['location']



