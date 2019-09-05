import sys
import time
import functools
import threading
from typing import List

from src.twitter_stream import TwitterStream
from src.resources_manager import ResourcesManager
from src.singleton import Singleton
from src.logger import Logger


class TwitterStreamManager(Singleton):

    def __init__(self):
        super().__init__()
        self.__streams: List[TwitterStream] = []
        self.__class__.__instance = self

    def init_streams(self):
        rm = ResourcesManager.get_instance()

        financial_tracks = ResourcesManager.get_batches(
            [*functools.reduce(lambda x, y: x + y, rm.financial_tracks.values())], length=ResourcesManager.BATCH_SIZE)
        stock_tracks = rm.stock_tracks

        nbr_streams = len(financial_tracks) + len(stock_tracks) + 1  # One for trend tracks

        tokens = rm.load_tokens()

        if nbr_streams > len(tokens) - 1:  # - 1 because we use one token for retrieving trend tracks
            Logger.get_instance().error(f'There is not enough tokens ({nbr_streams - len(tokens) + 1} token in less)')
            sys.exit(-1)

        streams, i = [], 1
        for j in range(len(financial_tracks)):
            token = ResourcesManager.create_token(tokens[str(i)])
            streams.append(TwitterStream(token=token, topic='Financial', tracks=financial_tracks[j]))
            i += 1

        for k, v in stock_tracks.items():
            token = ResourcesManager.create_token(tokens[str(i)])
            streams.append(TwitterStream(token=token, topic=f'Stock.{k}', tracks=v[j]))
            i += 1

        token = ResourcesManager.create_token(tokens[str(i)])
        rm.get_trend_tracks(token=token)
        streams.append(TwitterStream(token=token, topic='Trend'))

        self.__streams = streams

    def start_streams(self):
        for stream in self.__streams:
            stream.start()

    def update_trend_track(self, time_interval: int):
        def _update_trend_track(streams, _time_interval):
            while True:
                time.sleep(_time_interval)
                for stream in streams:
                    if stream.topic == 'Trend':
                        stream.stop()
                        stream.start()
                        Logger.get_instance().info('Trend tracks updated')
        try:
            t = threading.Thread(target=_update_trend_track, args=(self.__streams, time_interval))
            t.daemon = True  # We don't have to explicitly kill the thread when the program exits
            t.start()
        except Exception as e:
            Logger.get_instance().exception(f'Exception occurred: {e}')
            self.stop_streams()
            sys.exit(-1)

    def stop_streams(self):
        for stream in self.__streams:
            stream.stop()
