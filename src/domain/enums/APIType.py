from enum import Enum


class APIType(Enum):

    @classmethod
    def valid_apis(cls):
        return list(map(lambda api: api.value.lower(), cls))
