FROM python:3.15-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --require-hashes -r /requirements.txt --quiet

COPY entrypoint.py /entrypoint.py

RUN useradd -r -u 1001 sieve
USER sieve

ENTRYPOINT ["python3", "/entrypoint.py"]
