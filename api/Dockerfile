FROM python:3.10-slim

WORKDIR /api

COPY . ./

RUN pip install .

# create a non-root user and switch to it, for security.
RUN addgroup --system --gid 1001 "api-user"
RUN adduser --system --uid 1001 "api-user"
USER "api-user"

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0"]
