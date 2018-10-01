import configparser


class ImproperlyConfigured(RuntimeError):
    pass


class ConfigSection(dict):
    def __init__(self, iterable, *, name: str):
        self.name = name
        super().__init__(iterable)

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            raise ImproperlyConfigured(
                f"Section `{self.name}` is missing variable `{item}`"
            )


class Config:
    def __init__(self, filename: str):
        self.filename = filename
        self._config = configparser.ConfigParser()
        self._config.read(self.filename)

    def __getitem__(self, name: str) -> ConfigSection:
        try:
            return ConfigSection(self._config[name], name=name)
        except KeyError:
            raise ImproperlyConfigured(
                f"Section {name} is missing in `{self.filename}`"
            )


config = Config("config.ini")
