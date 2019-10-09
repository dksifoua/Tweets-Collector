import sys
import signal

from kafka.errors import NoBrokersAvailable

from src.twitter_stream_manager import TwitterStreamManager
from src.resources_manager import ResourcesManager
from src.logger import Logger

# TODO
#   Review stock tracks
#   Use confluent-kafka-python (more faster) than python-kafka


def signal_handler(sig, frame):
    global streams_manager
    streams_manager.stop_streams()
    Logger.get_instance().critical('Program stopped thank to Ctrl^C command!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    ResourcesManager.BOOTSTRAP_SERVERS = ['localhost:9092']
    ResourcesManager.STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'GS', 'WMT']

    streams_manager = TwitterStreamManager.get_instance()

    try:
        streams_manager.init_streams()
    except NoBrokersAvailable as e:
        Logger.get_instance().error(f'{e}')
        sys.exit(-1)

    streams_manager.start_streams()
    streams_manager.update_trend_tracks(time_interval=3600)
