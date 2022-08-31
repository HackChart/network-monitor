import subprocess
import platform
import re

# TODO: refactor into server/connection/handler classes
# read like RESULTS.SERVER.ID / RESULTS.SERVER.ISP / RESULTS.CONNECTION.UPLOAD / RESULTS.CONNECTION.LATENCY
# TODO: definitely name this class something less redundant
class SpeedtestWrapper:
    """Wrapper for Ookla's Speedtest CLI, currently only returns
    results as an object for ease of use"""
    def __init__(self):
        # check OS, run appropriate version of speedtest CLI
        self.os = platform.system()
        if self.os == 'Windows':
            results = subprocess.run('.\speedtest.exe', capture_output=True)
        elif self.os == 'Darwin':
            results = subprocess.run('./speedtest', capture_output=True)
        # convert stdout from byte string
        self.decoded_results = results.stdout.decode('UTF-8')
        print(self.decoded_results)

        # init attrs from captured results
        for line in self.decoded_results.split('\n'):
            if 'Server' in line:
                # FOR REFERENCE:
                # RESULT RETURNS "Server: ISP - City, St (id = \d)"
                # TODO: COMBINED REGEX TOO RIGID
                city_pattern = r"(\b\w*),"
                state_pattern = r"\b\w\w\b"
                id_pattern = r"id = (\d*)"
                # TODO: consider expanding to include more granular options for id and loc
                self.server = line.split(':')[1].strip()
            # TODO: REMOVE THIS LINE AFTER PARSING SERVER WITH REGEX
            elif 'ISP' in line:
                # expressed as str
                self.isp = line.split(':')[1].strip()
            elif 'Latency' in line:
                # FOR REFERENCE:
                # RESULT RETURNS "Latency:   129.42 ms   (7.09 ms jitter)"
                results = line.split(':')[1].strip()
                self.latency = float(results.split('ms')[0])
                self.jitter = float(results.split('(')[1].split(' ')[0])
            elif 'Download' in line:
                # TODO: don't use sizing for delimiter, could break on slow networks
                # TODO: DEFINITELY JUST USE REGEX YOU BRAINLET
                # FOR REFERENCE:
                # RESULT RETURNS Download:     8.52 Mbps (data used: 12.1 MB)
                # speed as float in Mbps
                self.download_speed = float(line.split(':')[1].split('Mbps')[0])
                # size as float in MB
                self.download_size = float(line.split(':')[2].split('MB')[0])
            elif 'Upload' in line:
                # TODO: REWORK WITH REGEX
                # FOR REFERENCE
                # Upload:    41.36 Mbps (data used: 70.2 MB)
                # speed as float in Mbps
                self.upload_speed = float(line.split(':')[1].split('Mbps')[0])
                # size as float in MB
                self.upload_size = float(line.split(':')[2].split('MB')[0])
            elif 'Packet Loss' in line:
                # Pulls latency out of results as \d.\d%
                latency_pattern = r"\b\d+\.?\d+%"
                self.packet_loss = re.search(latency_pattern, line)

    def __repr__(self):
        return self.decoded_results


if __name__ == '__main__':
    # TODO: remove later, for testing purposes only
    results = SpeedtestWrapper()
    print(results.upload_speed)
    print(results.download_speed)
    print(results)