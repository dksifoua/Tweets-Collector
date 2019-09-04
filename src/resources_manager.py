import sys
import json
from typing import List, Any

import tweepy


class ResourcesManager:
    WOEID = 23424977  # WOEID for USA
    STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'GS', 'WMT']

    def __init__(self):
        # Load stock tracks
        self._stock_tracks = {}
        for stock in ResourcesManager.STOCKS:
            self._stock_tracks[stock] = ResourcesManager.load_tracks('Stock', stock)

        # Load financial tracks
        self._financial_tracks = {}
        for track_type in ['acronyms', 'phrases', 'tracks']:
            self._financial_tracks[track_type] = ResourcesManager.load_tracks('Financial', track_type)

        #   Define trend tracks
        self._trend_tracks = []

        # Load tokens
        self._tokens = ResourcesManager.load_tokens()

    @staticmethod
    def get_trend_tracks(api: tweepy.API):
        if not api:
            print('Error while connecting to Twitter API')
            sys.exit(-1)
        trends = api.trends_place(ResourcesManager.WOEID)
        return [trend['name'] for trend in trends[0]['trends']]

    @staticmethod
    def load_tokens():
        try:
            with open('./resources/tokens/tokens.json', 'r') as file:
                return json.load(file)
        except Exception as e:
            print('Exception occurred:', e)
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
            print('Exception occurred:', e)
            import os
            print(os.getcwd(), os.listdir())
            sys.exit(-1)

    @staticmethod
    def get_batches(data: List[Any], length: int):
        batches, i = [], 0
        while True:
            batch = data[i:i + length]
            batches.append(batch)
            i += length
            if i > len(data):
                break
        return batches
