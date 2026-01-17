import time
import json
from datetime import datetime
import pandas as pd

class RTKMonitor:
    def __init__(self):
        self.points = []
        self.status = "Disconnected"
        self.fix_type = "Single"
        self.latitude = 23.0225  # Ahmedabad
        self.longitude = 72.5714
        self.altitude = 55.0
        self.sats = 12
        
    def update_data(self):
        import random
        self.status = "RTK Fixed" if random.randint(1,10) > 3 else "RTK Float"
        self.fix_type = self.status
        self.sats = random.randint(14,22)
        self.latitude += random.uniform(-0.0001, 0.0001)
        self.longitude += random.uniform(-0.0001, 0.0001)
        self.altitude += random.uniform(-0.5, 0.5)
        
        point = {
            'time': datetime.now().strftime('%H:%M:%S'),
            'lat': self.latitude,
            'lon': self.longitude, 
            'alt': self.altitude,
            'fix': self.fix_type,
            'sats': self.sats
        }
        self.points.append(point)
        if len(self.points) > 100:
            self.points.pop(0)
