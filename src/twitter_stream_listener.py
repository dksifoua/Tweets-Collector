import sys
import json
import asyncio

import tweepy
from kafka import KafkaProducer

from src.resources_manager import ResourcesManager
from src.utils import extract_features
from src.logger import Logger


class TwitterStreamListener(tweepy.streaming.StreamListener):

    def __init__(self, api: tweepy.API, topic: str, id_: int):
        tweepy.streaming.StreamListener.__init__(self, api)

        self.__id = id_
        self.__topic = topic
        # Asynchronous by default
        self.__producer = KafkaProducer(bootstrap_servers=ResourcesManager.BOOTSTRAP_SERVERS)

    def on_connect(self):
        Logger.get_instance().info(f'Stream listener is connected Twitter for topic {self.__topic}-{self.__id}')

    def on_data(self, raw_data):
        raw_data = json.loads(raw_data)
        rm = ResourcesManager.get_instance()

        # Extract features
        try:
            if raw_data['lang'] == 'en':
                tweet = extract_features(raw_data)
                if tweet is None:
                    return True
            else:
                return True
        except KeyError:
            return True

        # Strong filter to drop out noises
        if self.__topic == 'Financial':
            tracks = rm.financial_tracks
            contains_acronyms = [*map(tweet['text'].__contains__, tracks['acronyms'])]
            contains_phrases = [
                *map(tweet['text'].lower().__contains__, [*map(lambda x: x.lower(), tracks['phrases'])])]
            contains_words = [*map(tweet['text'].lower().__contains__, [*map(lambda x: x.lower(), tracks['words'])])]
            contains = any(contains_acronyms) or any(contains_phrases) or any(contains_words)
        elif self.__topic == 'Trend':
            tracks = rm.trend_tracks
            contains_ = [*map(tweet['text'].__contains__, tracks)]
            contains_lower = [*map(tweet['text'].lower().__contains__, [*map(lambda x: x.lower(), tracks)])]
            contains = any(contains_) or any(contains_lower)
        elif 'Stock' in self.__topic:
            stock = self.__topic.split('.')[1]
            tracks = rm.stock_tracks[stock]
            contains_ = [*map(tweet['text'].__contains__, tracks)]
            contains_lower = [*map(tweet['text'].lower().__contains__, [*map(lambda x: x.lower(), tracks)])]
            contains_name = [*map(tweet['user_name'].__contains__, tracks)]
            contains_screen_name = [*map(tweet['user_screen_name'].__contains__, tracks)]
            contains = any(contains_) or any(contains_lower) or any(contains_name) or any(contains_screen_name)
        else:
            Logger.get_instance().error(f'Unknown topic: {self.__topic}')
            sys.exit(-1)

        if contains is False:
            return True

        self.__producer.send(topic=self.__topic, value=json.dumps(tweet).encode('utf-8'),
                             key=self.__topic.encode('utf-8'))
        Logger.get_instance().debug(
            f"Topic: {self.__topic} | Created at: {tweet['created_at']} | User: {tweet['user_screen_name']}\n"
            f"{tweet['text']}\n"
            f"===============================================================================================")

    def on_error(self, status_code):
        Logger.get_instance().error(
            f'Error occurred for topic {self.__topic}-{self.__id} with status {status_code}.\n'
            f'For more information, please visit https://developer.twitter.com/en/docs/basics/response-codes')

    def on_timeout(self):
        Logger.get_instance().info('Stream connection times out')
