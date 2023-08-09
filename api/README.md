# Github Activity Monitor API
The API is a Python application that provides a REST API to query the data stored in the database by the ingestor. The API is implemented using Litestar. The documentation of Litestar can be found [here](https://litestar.dev/). The OpenAPI-based documentation of the endpoints are automatically generated. When running the API locally, the documentation can be found at:
- http://localhost:8000/schema (for ReDoc),
- http://localhost:8000/schema/swagger (for Swagger UI),
- http://localhost:8000/schema/elements (for Stoplight Elements)

Currently, the events that are ingested are:
- WatchEvent
- PullRequestEvent
- IssuesEvent

The current endpoints/metrics are currently implemented:
- A list of all repositories of events that have been ingested and have had at least 2 open pull requests.
- The average time between pull requests for a given repository.
- The total number of events grouped by the event type for a given offset. The offset determines how much time in **minutes** the events are selected.

## Environment Variables
### Required
None

### Optional

When using the API separately, you need additional environment variables to connect to a (PostgreSQL) database:
- `POSTGRES_HOST` - Hostname of the PostgreSQL database. Default: `"localhost"`
- `POSTGRES_PORT` - Port of the PostgreSQL database. Default: `5432`
- `POSTGRES_USER` - Username of the PostgreSQL database. Default: `"postgres"`
- `POSTGRES_PASSWORD` - Password of the PostgreSQL database. Default: `""`
- `POSTGRES_DB` - Name of the PostgreSQL database. Default: `"postgres"`

## Run Locally
### Using Docker
```bash
  docker build -t github-activity-monitor-api .
  docker run -it --rm --name github-activity-monitor-api -e POSTGRES_HOST=$POSTGRES_HOST -e POSTGRES_USER=$POSTGRES_USER -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -e POSTGRES_DB=$POSTGRES_DB -p 8000:8000 github-activity-monitor-api
```

When using running a PostgreSQL database in a seperate Docker container, you can set the `POSTGRES_HOST` environment variable to the IP address of the container with:
```bash
  export POSTGRES_HOST=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name_or_id>)
```

### Using Python
Make sure that the PostgreSQL database is running and the environment variables are set. Then run:
```bash
  pip install .
  uvicorn app:app
```

## Unit Tests

TODO
