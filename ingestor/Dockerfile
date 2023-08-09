FROM python:3.10-slim

WORKDIR /ingestor

COPY . ./

RUN pip install .

# create a non-root user and switch to it, for security.
RUN addgroup --system --gid 1001 "ingestor"
RUN adduser --system --uid 1001 "ingestor"
USER "ingestor"

ENTRYPOINT ["python", "main.py"]
