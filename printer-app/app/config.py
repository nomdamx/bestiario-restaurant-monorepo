
from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
        
        self.API_URL = os.environ.get("API_URL")
        self.IP_PRINTER = os.environ.get("IP_PRINTER")
        self.PORT_PRINTER =os.environ.get("PORT_PRINTER")
        
        self.APP_TITLE = "Bestiario Tickets"
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 500
        self.WINDOW_MIN_WIDTH = 600
        self.WINDOW_MIN_HEIGHT = 400
        self.MAX_RETRIES = 3

CONFIG = Config()