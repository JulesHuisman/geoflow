import os
import subprocess
import logging
from typing import Any, List
from airflow.hooks.base import BaseHook


class IngestPostgisHook(BaseHook):
    def __init__(self,
                 command: List[str],
                 database_schema: str,
                 conn_id: str = 'geoflow_db'):
        self._command = []
        self._conn_id = conn_id
        self._database_schema = database_schema

        # Get the connection using the connectin API
        self._connection = self.get_connection(self._conn_id)

        self._command += ['ogr2ogr']
        self._command += ['-f']
        self._command += ['PostgreSQL']

        # Concat the database connection string
        db_connection = [
            f'PG:dbname={self._connection.schema}',
            f'host={self._connection.host}',
            f'port={self._connection.port}',
            f'user={self._connection.login}',
            f'password={self._connection.password}',
            f'active_schema={self._database_schema}'
        ]

        self._command += [' '.join(db_connection)]

        # Make sure a command is supplied
        assert len(command) > 0, 'Make sure you supplied a command'

        # Add the higher level command
        self._command.extend(command)

    def get_conn(self) -> Any:
        pass

    def run_command(self):
        # Log the command
        print(self._command)

        # Run the command in a subprocess
        self._sp = subprocess.Popen(self._command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    preexec_fn=os.setpgrp)

        # Run the command synchronous
        std_out, std_err = self._sp.communicate()

        # Make sure there are no errors
        assert std_err == b'', std_err

        print(std_out)

    def kill(self) -> None:
        """Kill transformation"""
        if self._sp and self._sp.poll() is None:
            logging.log('Killing ogr to ogr command')
            self._sp.kill()
