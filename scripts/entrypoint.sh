#!/usr/bin/env bash
airflow db init

# Make optional
airflow users create -e geo@flow.nl -f geo -l flow -p geoflow -r Admin -u geoflow

airflow webserver
