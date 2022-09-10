import subprocess
import json


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
