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
        Logger.get_instance().info(f'Stream listener is connected Twitter for topic {self.__topic}-{self.__id}')

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        Logger.get_instance().error(
            f'Error occurred for topic {self.__topic}-{self.__id} with status {status_code}.\n For more infos, please visit https://developer.twitter.com/en/docs/basics/response-codes')

    def on_timeout(self):
        Logger.get_instance().info('Stream connection times out')
