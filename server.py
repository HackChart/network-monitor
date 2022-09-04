import re

# TODO: DO MORE RESEARCH INTO SERVER/ISP BREAKDOWN
# RESULTS INCONSISTENT
#      Server: Rock Island Communications - Seattle, WA (id = 26805)
#         ISP: Apple


class Server:
    def __init__(self):
        self.isp = None
        self.city = None
        self.state = None
        self.location = f"{self.city}, {self.state}"
        self.id = None
