import sys
import json
import threading
from typing import Dict, List, Any

import tweepy

from src.singleton import Singleton
from src.token import Token
from src.logger import Logger


class ResourcesManager(Singleton):

    WOEID = 23424977  # WOEID for USA
    STOCKS = ['AAPL', 'MSFT', 'GOOGL']  # , 'GS', 'WMT'
    BATCH_SIZE = 390
    LOCK = threading.RLock()

    def __init__(self):
        super().__init__()

        # Load stock tracks
        self.__stock_tracks = {}
        for stock in self.__class__.STOCKS:
            self.__stock_tracks[stock] = self.__class__.load_tracks('Stock', stock)

        # Load financial tracks
        self.__financial_tracks = {}
        for track_type in ['acronyms', 'phrases', 'words']:
            self.__financial_tracks[track_type] = self.__class__.load_tracks('Financial', track_type)

        #   Define trend tracks
        self.__trend_tracks = []

        # Load tokens
        self.__tokens = self.__class__.load_tokens()

        self.__class__.__instance = self

    @property
    def stock_tracks(self):
        return self.__stock_tracks

    @property
    def financial_tracks(self):
        return self.__financial_tracks

    @property
    def trend_tracks(self):
        return self.__trend_tracks

    @trend_tracks.setter
    def trend_tracks(self, tracks: List[str]):
        self.__trend_tracks = tracks

    @staticmethod
    def create_token(token: Dict[str, str]) -> Token:
        return Token(api_key=token['api_key'], api_secret=token['api_secret'],
                     access_key=token['access_key'], access_secret=token['access_secret'])

    def get_trend_tracks(self, token: Token):
        auth = tweepy.OAuthHandler(token.api_key, token.api_secret)
        auth.set_access_token(token.access_key, token.access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        if not api:
            print('Error while connecting to Twitter API')
            sys.exit(-1)

        trends = api.trends_place(ResourcesManager.WOEID)
        self.__trend_tracks = [' ' + trend['name'] + ' ' for trend in trends[0]['trends']]

    @staticmethod
    def load_tokens() -> Dict[str, str]:
        try:
            with open('./resources/tokens/tokens.json', 'r') as file:
                return json.load(file)
        except Exception as e:
            Logger.get_instance().exception(f'Exception occurred: {e}')
            sys.exit(-1)

    @staticmethod
    def load_tracks(folder: str, filename: str) -> List[str]:
        try:
            with open(f'./resources/tracks/{folder}/{filename}.txt', 'r') as file:
                tracks = file.readlines()
                tracks = [*map(lambda track: track.split('\n')[0], tracks)]
                tracks = [*set(tracks)]
                return tracks
        except Exception as e:
            Logger.get_instance().exception(f'Exception occurred: {e}')
            sys.exit(-1)

    @staticmethod
    def get_batches(data: List[Any], length: int) -> List[List[str]]:
        batches, i = [], 0
        while True:
            batch = data[i:i + length]
            batches.append(batch)
            i += length
            if i > len(data):
                break
        return batches
