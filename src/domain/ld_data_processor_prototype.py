from abc import abstractmethod


class LDDataProcessorPrototype:
    def __init__(self, config):
        self._config = config
