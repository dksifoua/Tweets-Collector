import tweepy
from kafka import KafkaProducer

from src.logger import Logger


class TwitterStreamListener(tweepy.streaming.StreamListener):

    def __init__(self, api: tweepy.API, topic: str, id_: int):
        tweepy.streaming.StreamListener.__init__(self, api)

        self.__id = id_
        self.__topic = topic
        # self.__producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    def on_connect(self):
        Logger.get_instance().info(f'Stream listener  is connected Twitter for topic {self.__id}-{self.__topic}')

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        Logger.get_instance().error(f'Error occurred with status {status_code}')

    def on_timeout(self):
        Logger.get_instance().info('Stream connection times out')
