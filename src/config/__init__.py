class AppConfig:
    def __init__(self, path: str):
        import configparser
        self.path = path
        self.__config = configparser.ConfigParser()
        self.__config.read(path)

    def __getitem__(self, key: str):
        return self.__config[key]

    @property
    def valid(self):
        return 'api_key' in self['kadebot']
