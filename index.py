from src.resources_manager import ResourcesManager

if __name__ == '__main__':
    # if len([*filter(lambda x: len(x[1]) > ResourcesManager.BATCH_SIZE, ResourcesManager.STOCK_TRACKS.items())]) > 0:
    #     print('Length of each stock track list must be least or equal than BATCH_SIZE')
    #     sys.exit(-1)
    res_manger = ResourcesManager()
