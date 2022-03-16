import time

from src.decorators.loggable import logger
from src.models.pipeline import Pipeline
from src.view_models.configuration_view_model import ConfigurationViewModel
from src.models.associations_processor import GWASCatalogProcessor
from src.models.ldmatrix_processor import LDMatrixProcessor


@logger
class ProjectViewModel:

    def __init__(self, user_project_folder):
        # ToDo - add mtag file path and column names for variant and chromosome into config (with user warnings)
        self._config = ConfigurationViewModel(user_project_folder)
        self._pipeline = None

    @property
    def pipeline(self):
        return self._pipeline

    @pipeline.setter
    def pipeline(self, pipeline):
        self._pipeline = pipeline

    def run(self, id_term, name_term):
        logger = self._config.logger_config()
        associations_config = self._config.associations_config()
        ld_config = self._config.ld_config()
        self._pipeline = self._run_pipeline(associations_config, ld_config, logger, id_term, name_term)
        return 0

    def _run_pipeline(self, associations_config, ld_config, logger, id_term, name_term):
        start = time.time()
        self._log_message(logger, f"GWAS Pipeline started.")
        association_processor = GWASCatalogProcessor(associations_config)
        ld_processor = LDMatrixProcessor(ld_config)
        pipeline = Pipeline(association_processor, ld_processor)
        pipeline.run(id_term, name_term)
        duration = time.time() - start
        self._log_message(logger, f"Successfully run GWAS Pipeline in {duration:0.3f}s")
        return pipeline

    def _log_message(self, logger, message):
        logger.info(message)
