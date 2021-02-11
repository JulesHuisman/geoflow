FROM apache/airflow:2.0.0-python3.8

USER root

ENV PATH="/home/airflow/miniconda3/bin:${PATH}"
ARG PATH="/home/airflow/miniconda3/bin:${PATH}"

RUN apt-get update
RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

USER airflow

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /home/airflow/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 

RUN conda --version

RUN conda install gdal

COPY ./scripts/entrypoint.sh ./scripts/entrypoint.sh