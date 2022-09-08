import subprocess
import platform
import re
from server import Server
from connection import Connection

# PASSED BASIC TESTING
# TODO: TYPE CAST DATA INTO CORRECT DATATYPE / VALIDATE DATA
# TODO: IMPLEMENT ERROR HANDLING IN THE CASE OF NO MATCH / NOT AS MANY MATCHES FOUND AS EXPECTED
# TODO: REFACTOR INTO HANDLER


class Speedtest:
    """Wrapper for Ookla's Speedtest CLI, currently only returns
    results as an object for ease of use"""
    def __init__(self):
        # check OS, run appropriate version of speedtest CLI
        # TODO: OBFUSCATE LATER, LOOK FOR UTILITY IN PATH / DOWNLOAD / ACCEPT USER PATH
        self.os = platform.system()
        if self.os == 'Windows':
            results = subprocess.run('.\speedtest.exe', capture_output=True)
        elif self.os == 'Darwin':
            results = subprocess.run('./speedtest', capture_output=True)
        # convert stdout from byte string
        self.decoded_results = results.stdout.decode('UTF-8')
        print(self.decoded_results)

        # ----- CREATE RESULT OBJECTS ----- #
        # init instances
        self.server = Server()
        self.connection = Connection()
        # define over-arching patterns
        connection_pattern = r"(\b\d*\.?\d*) \w+"

        # CREATE SERVER INSTANCE ATTRS
        for line in self.decoded_results.split('\n'):
            # TODO: ATTR INITS NEED EXCEPTION HANDLING (maybe just check all nonetypes before sub?
            if 'Server' in line:
                # Define search patterns (some need to be subbed to remove delimiters
                owner_pattern = r": (\b[\w\s.-]*\b) -"   # sub 1
                city_pattern = r"- (\b[\w\s.-]*\b),"   # sub 1
                state_pattern = r"\b[A-Z][A-Z]\b"   # no subscript
                id_pattern = r"id = (\d*)"   # sub [1]
                # Assign attrs ** SOME SUBSCRIPTED TO REMOVE DELIMITERS **
                self.server.owner = re.search(owner_pattern, line)[1]
                self.server.city = re.search(city_pattern, line)[1]
                self.server.state = re.search(state_pattern, line)[0]
                self.server.location = f"{self.server.city}, {self.server.state}"
                self.server.id = re.search(id_pattern, line)[1]
            elif 'ISP' in line:
                isp_pattern = r": (\b[\w\s.-]*\b)"
                self.server.isp = re.search(isp_pattern, line)[1]   # sub 1 remove delimiter
            elif 'Latency' in line:
                """LATENCY VALUES EXPRESSED IN MS"""
                # Parse out latency and jitter
                # TODO: PROBABLY CHECK THIS LOGIC AGAIN 🙃
                # remove any potential empty match strings
                parsed_latency = [i for i in re.findall(connection_pattern, line) if i]   # should find latency & jitter at [0]/[1]
                self.connection.latency = parsed_latency[0]
                self.connection.jitter = parsed_latency[1]
            elif 'Download' in line:
                """
                DOWNLOAD SPEED EXPRESSED IN Mbps
                DOWNLOAD SIZE EXPRESSED IN MB
                """
                parsed_download = [i for i in re.findall(connection_pattern, line) if i]   # should remove any false matches
                self.connection.download_speed = parsed_download[0]
                self.connection.download_size = parsed_download[1]
            elif 'Upload' in line:
                """
                UPLOAD SPEED EXPRESSED IN Mbps
                UPLOAD SIZE EXPRESSED IN MB
                """
                parsed_upload = [i for i in re.findall(connection_pattern, line) if i]    # remove false matches
                self.connection.upload_speed = parsed_upload[0]
                self.connection.upload_size = parsed_upload[1]
            elif 'Packet Loss' in line:
                # Pulls latency out of results as \d.\d%
                loss_pattern = r"\b\d+\.?\d+%"
                self.connection.packet_loss = re.search(loss_pattern, line)[0]

    def __repr__(self):
        return self.decoded_results
