class Server:
    def __init__(self):
        self.isp = None
        self.owner = None
        self.city = None
        self.state = None
        self.location = f"{self.city}, {self.state}"
        self.id = None
