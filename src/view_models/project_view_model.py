import time

from src.decorators.loggable import logger
from src.models.pipeline import Pipeline
from src.view_models.configuration_view_model import ConfigurationViewModel


@logger
class ProjectViewModel:

    def __init__(self):
        self._config = ConfigurationViewModel()
        self._pipeline = None

    @property
    def pipeline(self):
        return self._pipeline

    @pipeline.setter
    def pipeline(self, pipeline):
        self._pipeline = pipeline

    def run(self, id_term, name_term, output_path):
        logger = self._config.logger_config()
        app_config = self._config.application_config()
        self._pipeline = self._run_pipeline(app_config, logger, id_term, name_term, output_path)
        return 0

    def _run_pipeline(self, app_config, logger, id_term, name_term, output_path):
        start = time.time()
        self._log_message(logger, f"GWAS Pipeline started.")
        pipeline = Pipeline(app_config)
        pipeline.run(id_term, name_term, output_path)
        duration = time.time() - start
        self._log_message(logger, f"Successfully run GWAS Pipeline in {duration:0.3f}s")
        return pipeline

    def _log_message(self, logger, message):
        logger.info(message)
