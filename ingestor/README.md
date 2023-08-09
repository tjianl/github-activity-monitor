# Github Activity Monitor Ingestor
The ingestor is a Python application that polls the GitHub Events API and stores the data in a (PostgreSQL) database. The documentation of the Github Events API can be found [here](https://docs.github.com/en/rest/activity/events). Currently, the ingestor only stores the following events:
 - WatchEvent
 - PullRequestEvent
 - IssuesEvent


## Requirements
| Name | Version |
|-|-|
| Docker Engine | >=20.10.13 |
| Python | >=3.10.0 |

## Environment Variables
### Required
None

### Optional

`GITHUB_TOKEN` - GitHub API token, which allows the ingestor to increase the API call limit 60 to 5000 requests per hour. Documentation for generating the token can be found [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

When using the ingestor separately, you need additional environment variables to connect to a (PostgreSQL) database:

`POSTGRES_HOST` - Hostname of the PostgreSQL database. Default: `"localhost"`
`POSTGRES_PORT` - Port of the PostgreSQL database. Default: `5432`
`POSTGRES_USER` - Username of the PostgreSQL database. Default: `"postgres"`
`POSTGRES_PASSWORD` - Password of the PostgreSQL database. Default: `""`
`POSTGRES_DB` - Name of the PostgreSQL database. Default: `"postgres"`

`MAX_POLL_INTERVAL` - Maximum interval in seconds in which the GitHub Events API is polled

## Run Locally
### Using Docker
```bash
  docker build -t github-activity-monitor-ingestor .
  docker run -it --rm --name github-activity-monitor-ingestor -e POSTGRES_HOST=$POSTGRES_HOST -e POSTGRES_USER=$POSTGRES_USER -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -e POSTGRES_DB=$POSTGRES_DB github-activity-monitor-ingestor
```

When using running a PostgreSQL database in a seperate Docker container, you can set the `POSTGRES_HOST` environment variable to the IP address of the container with:
```bash
  export POSTGRES_HOST=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name_or_id>)
```

### Using Python
Make sure that the PostgreSQL database is running and the environment variables are set. Then run:
```bash
  pip install .
  python -m main.py
```

## Unit Tests
Install test dependencies and run unit tests with:
```bash
  pip install ".[test]"
  python -m pytest
```

## Work in Progress
It is also possible to run the ingestor and storing the polled events in a Redis database. It works, but the API is not implemented using Redis yet. To run the ingestor with Redis, you can follow the following steps:

If you don't have a Redis database running, you can start with:
```bash
  docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

Set the `REDIS_HOST` environment variable to the IP address of the Redis container with:
```bash
  export REDIS_HOST=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-stack)
```

Then run the ingestor using Docker with:
```bash
  docker run -it --rm --name github-activity-monitor-ingestor -e REDIS_HOST=$REDIS_HOST github-activity-monitor-ingestor --db-client=redis
```

Or just regular Python:
```bash
  python -m main.py --db-client=redis
```

You can inspect the Redis database with RedisInsight, which is running on port 8001: http://localhost:8001/redis-stack/browser
