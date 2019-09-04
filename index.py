from src.resources_manager import ResourcesManager
from src.logger import Logger

if __name__ == '__main__':
    # if len([*filter(lambda x: len(x[1]) > ResourcesManager.BATCH_SIZE, ResourcesManager.STOCK_TRACKS.items())]) > 0:
    #     print('Length of each stock track list must be least or equal than BATCH_SIZE')
    #     sys.exit(-1)
    res_mgr1 = ResourcesManager.get_instance()
    res_mgr2 = ResourcesManager.get_instance()

    log1 = Logger.get_instance()
    log2 = Logger.get_instance()

    assert res_mgr1 is res_mgr2, 'error in ResourcesManager!'
    assert log1 is log2, 'error in ResourcesManager!'
