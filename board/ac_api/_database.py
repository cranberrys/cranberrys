import os
import pathlib
import shelve


class DataManager:
    def __init__(self, key, collection):
        self.__dir = pathlib.Path('data')
        if not os.path.exists(self.__dir):
            os.mkdir(self.__dir)
        self.__key = key
        self.__filepath = self.__dir / collection
        self.__value = None

    def __enter__(self):
        dm = shelve.open(str(self.__filepath))
        self.__value = dm.get(self.__key, {})
        dm.close()
        return self.__value

    def __exit__(self, exit_type, exit_value, exit_trace):
        dm = shelve.open(str(self.__filepath))
        dm[self.__key] = self.__value
        dm.close()
