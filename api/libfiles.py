class FileRecord(object):
    def __init__(self, id, name, path):
        self.__id = id
        self.__name = name
        self.__path = path
        
    @property
    def id(self):
        return self.__id
        
    @property
    def name(self):
        return self.__name
        
    @property
    def path(self):
        return self.__path
