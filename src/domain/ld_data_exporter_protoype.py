from abc import abstractmethod


class LDDataExporterPrototype:
    def __init__(self, config):
        self._config = config
