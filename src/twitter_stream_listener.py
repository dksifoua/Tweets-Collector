import sys
import json

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
        # self.__producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

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

        # TODO
        #   Filter by tracks

        # self.__producer.send(topic=self.__topic, value=str(tweet).encode('utf-8'), key=self.__topic.encode('utf-8'))
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
