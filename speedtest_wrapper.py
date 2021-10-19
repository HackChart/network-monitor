import subprocess


class SpeedtestWrapper:
    """Wrapper for Ookla's Speedtest CLI, currently only returns
    results as an object for ease of use"""
    def __init__(self):
        """Run test and instantiate result attrs"""
        results = subprocess.run('./speedtest', capture_output=True)
        # convert stdout from byte string
        decoded_results = results.stdout.decode('UTF-8')

        # init attrs
        for line in decoded_results.split('\n'):
            if 'Server' in line:
                # TODO: consider expanding to include more granular options for id and loc
                self.server = line.split(':')[1].strip()
            elif 'ISP' in line:
                # expressed as str
                self.isp = line.split(':')[1].strip()
            elif 'Latency' in line:
                # latency values expressed as float in ms
                results = line.split(':')[1].strip()
                self.latency = float(results.split('ms')[0])
                self.jitter = float(results.split('(')[1].split(' ')[0])
            elif 'Download' in line:
                # TODO: don't use sizing for delimiter, could break on slow networks
                # speed as float in Mbps
                self.download_speed = float(line.split(':')[1].split('Mbps')[0])
                # size as float in MB
                self.download_size = float(line.split(':')[2].split('MB')[0])
            elif 'Upload' in line:
                # TODO: change sizing
                # speed as float in Mbps
                self.download_speed = float(line.split(':')[1].split('Mbps')[0])
                # size as float in MB
                self.download_size = float(line.split(':')[2].split('MB')[0])
            elif 'Packet Loss' in line:
                # TODO: implement handling for packet loss
                pass
