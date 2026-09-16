FROM python:3.14-slim@sha256:cad9a2c871761c413caa6fdd6441c783451e740a48aaeba60ae62a8b53525ef6

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --require-hashes -r /requirements.txt --quiet

COPY entrypoint.py /entrypoint.py

RUN useradd -r -u 1001 sieve
USER sieve

ENTRYPOINT ["python3", "/entrypoint.py"]
