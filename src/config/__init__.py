import configparser


class AppConfig:
    def __init__(self, path: str):
        """Reads a .ini configuration file.

        Arguments:
            path {str} -- The path to the configuration to be read.
        """

        import configparser
        self.path = path
        self.__config = configparser.ConfigParser()
        self.__config.read(path)

    def __getitem__(self, key: str) -> configparser.SectionProxy:
        """Retrieves a named section from the app configuration.

        Arguments:
            key {str} -- The section of the configuration to be obtained.

        Returns:
            configparser.SectionProxy -- The desired section from the config, acts like a dictionary.
        """

        return self.__config[key]

    @property
    def valid(self) -> bool:
        """Indicates whether the read config is valid.
        
        Returns:
            bool -- True if the config is valid, False otherwise.
        """

        return 'api_key' in self['kadebot']
