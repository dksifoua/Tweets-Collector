import sys
import functools
from src.twitter_stream import TwitterStream
from src.resources_manager import ResourcesManager
from src.singleton import Singleton
from src.logger import Logger


class TwitterStreamManager(Singleton):

    def __init__(self):
        super().__init__()
        self.__streams = []
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

    def stop_streams(self):
        for stream in self.__streams:
            stream.stop()
