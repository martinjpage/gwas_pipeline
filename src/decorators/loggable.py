import logging


def logger(class_):
    class_.logger = logging.getLogger("gwas_pipeline." + class_.__name__)
    return class_
