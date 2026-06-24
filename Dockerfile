FROM python:3.11-slim

RUN pip install --no-cache-dir semgrep requests --quiet

COPY entrypoint.py /entrypoint.py

ENTRYPOINT ["python3", "/entrypoint.py"]
