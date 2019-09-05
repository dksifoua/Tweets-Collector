import time

from src.twitter_stream_manager import TwitterStreamManager

if __name__ == '__main__':
    streams_manager = TwitterStreamManager.get_instance()

    streams_manager.init_streams()
    streams_manager.start_streams()
    time.sleep(10)
    streams_manager.stop_streams()
