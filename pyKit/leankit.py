import requests
import json
import itertools
import aiohttp
import asyncio

__author__ = 'Harry Lees'
__version__ = '1.0'

class connect:
    parameters = {
        'board' : '', # sets the board ID to be queried - filled in later by the program
        'limit' : '100000', # sets the limit on the number of cards that can be queried at a time
    }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self

    def __init__(self, domain, username, password):        
        self.authorization = username, password
        self.domain = domain

    @staticmethod
    def checkStatusCode(leankitData):
        if leankitData.status_code == 401:
            raise ConnectionRefusedError('Unauthorized, please check username and password')
        elif leankitData.status_code != 200:
            raise Exception('An unexpected error occurred')
        
        return True

    def getBoardIDs(self):
        boards = requests.get(f'https://{self.domain}.leankit.com/io/board', auth = self.authorization)
        
        if self.checkStatusCode(boards):
            return [(board['id'], board['title']) for board in json.loads(boards.text)['boards']]

    def getBoardData(self, boardID):
        self.parameters['board'] = boardID

        try:
            leankitData = requests.get(f'http://{self.domain}.leankit.com/io/card', params = self.parameters, auth = self.authorization)
        except Exception as exception:
            raise ConnectionError(f'Unable to make request: {exception}')

        if self.checkStatusCode(leankitData):
            return json.loads(leankitData.text)
