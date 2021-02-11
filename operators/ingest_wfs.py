from airflow.utils.decorators import apply_defaults
from geoflow.operators.ingest_postgis_operator import IngestPostgisOperator


class IngestWFSOperator(IngestPostgisOperator):
    ui_color = '#1890FF'
    ui_fgcolor = '#fff'

    @apply_defaults
    def __init__(
            self,
            wfs_url: str,
            **kwargs) -> None:

        super().__init__(
            source_command=[f'WFS:{wfs_url}'],
            ** kwargs
        )
