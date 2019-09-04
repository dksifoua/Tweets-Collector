import sys
import json
from typing import Dict, List, Any

import tweepy

from src.singleton import Singleton
from src.logger import Logger


class ResourcesManager(Singleton):

    WOEID = 23424977  # WOEID for USA
    STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'GS', 'WMT']

    def __init__(self):
        super().__init__()

        # Load stock tracks
        self.__stock_tracks = {}
        for stock in self.__class__.STOCKS:
            self.__stock_tracks[stock] = self.__class__.load_tracks('Stock', stock)

        # Load financial tracks
        self.__financial_tracks = {}
        for track_type in ['acronyms', 'phrases', 'tracks']:
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
    def get_trend_tracks(api: tweepy.API) -> List[str]:
        if not api:
            print('Error while connecting to Twitter API')
            sys.exit(-1)
        trends = api.trends_place(ResourcesManager.WOEID)
        return [' ' + trend['name'] + ' ' for trend in trends[0]['trends']]

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
