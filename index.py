import sys
import signal

from src.twitter_stream_manager import TwitterStreamManager
from src.resources_manager import ResourcesManager
from src.logger import Logger


if __name__ == '__main__':
    def signal_handler(sig, frame):
        global streams_manager
        streams_manager.stop_streams()
        Logger.get_instance().critical('Program stopped thank to Ctrl^C command!')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    streams_manager = TwitterStreamManager.get_instance()
    # print(ResourcesManager.get_instance().stock_tracks['AAPL'])

    streams_manager.init_streams()
    streams_manager.start_streams()
    streams_manager.update_trend_track(time_interval=3600)
