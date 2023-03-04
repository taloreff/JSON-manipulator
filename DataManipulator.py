import json
from datetime import datetime
from pathlib import Path
from dateutil import parser

class DataManipulator:
    def __init__(self, path:Path):
        self.path = path
        try:
            with path.open() as file:
                self.data = json.load(file)
        except ValueError:
            print("Bad input")
            
        
    def manipulate(self):
        new_data = {}
        for key,value in self.data.items():
            if isinstance(value, str):
                try:
                    if len(value) == 19  and (':' in value or '/' in value):  #type: datetime without UTC
                        new_value = datetime.strptime(value, '%Y/%m/%d %H:%M:%S').replace(year=2021).strftime('%Y/%m/%d %H:%M:%S')
                        
                    elif len(value) == 20  and ':' in value and '/' in value:  #type: datetime with UTC
                        new_value = parser.isoparse(value.replace('/', '-')).replace(year=2021).strftime('%Y/%m/%d %H:%M:%S%z') 
                    
                    else: #type: string
                        new_value = value.replace(' ', '').replace('\t' , '').replace('\n', '').replace('\r', '')[::-1]
                except ValueError:
                    continue
                                
            elif isinstance(value, list): #type: list
                new_value = []
                for v in value:
                    if v not in new_value:
                        new_value.append(v)
            
            if isinstance(value, str) or isinstance(value, list):
                new_data[key] = new_value
                
        self.data = new_data
        
    def save(self, path:Path):
        with path.open("w") as file:
            json.dump(self.data, file, indent=2)                    