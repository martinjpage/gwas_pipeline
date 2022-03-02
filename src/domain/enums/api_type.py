from enum import Enum


class APIType(Enum):
    gwas_catalog = "gwas_catalog"

    @staticmethod
    def valid_apis():
        return list(map(lambda api: api.value.lower(), APIType))
