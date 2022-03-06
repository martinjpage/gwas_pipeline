from abc import abstractmethod


class AssociationsDataProcessor:

    def __init__(self, key):
        self._key = key
        self._association_names = ['variant', 'risk_allele', 'p_value', "p_val_annotation", "RAF", "OR", "CI",
                                   "reported_genes", "chromosome_name", "chromosome_position", "reported_trait",
                                   "study"]

    @abstractmethod
    def extract_data(self, raw_data):
        pass

    @abstractmethod
    def _get_variant(self, data):
        pass

    @abstractmethod
    def _get_risk_allele(self, data):
        pass

    @abstractmethod
    def _get_p_value(self, data):
        pass

    @abstractmethod
    def _get_p_val_annotation(self, data):
        pass

    @abstractmethod
    def _get_raf(self, data):
        pass

    @abstractmethod
    def _get_or(self, data):
        pass

    @abstractmethod
    def _get_ci(self, data):
        pass

    @abstractmethod
    def _get_reported_genes(self, data):
        pass

    @abstractmethod
    def _get_chromosome_name(self, data):
        pass

    @abstractmethod
    def _get_chromosome_position(self, data):
        pass

    @abstractmethod
    def _get_reported_trait(self, data):
        pass

    @abstractmethod
    def _get_study_id(self, data):
        pass
