import requests
import datetime
from dataclasses import dataclass
from enum import Enum


class schedule_type(Enum):
    REGULAR = 0
    BANKARA = 1
    X = 2
    LEAGUE = 3
    COOP = 4
    FEST = 5

class rule(Enum):
    TURF_WAR = 0
    GOAL = 1
    LOFT = 2
    CLAM = 3
    AREA = 4

@dataclass
class stage:
    id: int
    name: str
    image: str

@dataclass
class match_setting:
    rule: rule
    stages: list[stage]

@dataclass
class schedule_node:
    start_time: datetime.datetime
    end_time: datetime.datetime
    match_settings: list[match_setting]

@dataclass
class schedule:
    type: schedule_type
    nodes: list[schedule_node] 

class s3api:
    def __init__(self):
        self.url = 'https://splatoon3.ink/data/'
    
    def get_schedules(self) -> dict:
        response:dict = requests.get(f'{self.url}schedules.json').json()['data']
        schedule = set()
        for key,value in response.items():
            if 'schedule' in key.lower():
                self._parse_schedule(value)
    
    def _parse_schedule(self, nodes: dict) -> schedule:
        schedule_nodes = []
        for x in nodes:
            schedule_nodes.append(self._parse_node(x))

    def _parse_node(self, node):
        return schedule_node(self._parse_time(node['startTime']), self._parse_time(node['endTime']), )
    
    def _parse_time(self, time: str) -> datetime.datetime:
        return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')


if __name__ == "__main__":
    test = s3api()
    x = (test.get_schedules())
    print(x)