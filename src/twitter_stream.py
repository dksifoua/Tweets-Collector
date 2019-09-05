import sys
import functools
from typing import List

import tweepy

from src.twitter_stream_listener import TwitterStreamListener
from src.resources_manager import ResourcesManager
from src.token import Token
from src.logger import Logger


class TwitterStream:
    _id = 1

    def __init__(self, token: Token, topic: str, tracks: List[str] = None):
        auth = tweepy.OAuthHandler(token.api_key, token.api_secret)
        auth.set_access_token(token.access_key, token.access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        if not api:
            Logger.get_instance().error(f'Problem while connecting to Twitter API | {topic}')

        self.__id = self.__class__._id
        self.__topic = topic
        self.__tracks = tracks

        stream_listener = TwitterStreamListener(api=api, topic=topic, id_=self.__id)
        self.__stream = tweepy.Stream(auth=auth, listener=stream_listener, tweet_mode='extended')

        self.__class__._id += 1

    @property
    def topic(self):
        return self.__topic

    @property
    def stream(self):
        return self.__stream

    def start(self):
        rm = ResourcesManager.get_instance()

        if self.__topic == 'Trend':
            if self.__tracks is None:
                tracks = rm.trend_tracks
            else:
                Logger.get_instance().error(f'Error occurred: the topic is Trend but the corresponding is not None')
                sys.exit(-1)
        else:
            tracks = self.__tracks

        self.__stream.filter(track=tracks, is_async=True)
        Logger.get_instance().info(f'Stream {self.__topic}:{self.__id} started.')

    def stop(self):
        self.__stream.running = False
        Logger.get_instance().info(f'Stream {self.__topic}:{self.__id} stopped.')
