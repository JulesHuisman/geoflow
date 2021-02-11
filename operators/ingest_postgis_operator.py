from typing import Any, Dict, List, Optional
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from geoflow.hooks.ingest_postgis_hook import IngestPostgisHook


class IngestPostgisOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            source_command: List[str],
            database_schema: str = 'staging',
            **kwargs) -> None:
        """Ingest data to a postgis database, calls the ingestion postgis hook.

        Args:
            source_command (List[str]): The source part of the ogr2ogr command
            database_schema (str, optional): To which postgres schema you want to ingest the data
        """
        super().__init__(**kwargs)
        self._command: List[str] = []
        self._hook: Optional[IngestPostgisHook] = None
        self._source_command = source_command
        self._database_schema = database_schema

    def _construct_command(self):
        self._command.extend(self._source_command)
        self._command += ['-nlt']
        self._command += ['PROMOTE_TO_MULTI']
        self._command += ['-lco']
        self._command += ['precision=NO']
        self._command += ['-overwrite']

    def execute(self, context: Dict[str, Any]) -> None:
        """Use the IngestPostgisHook to execute the command

        Args:
            context (Dict[str, Any]): Airflow context
        """
        self._construct_command()
        self._hook = IngestPostgisHook(
            command=self._command,
            database_schema=self._database_schema
        )

        # Run the command
        self._hook.run_command()

    def on_kill(self):
        """
        When the Airflow task is killed
        """
        if self._hook is not None:
            self._hook.kill()
