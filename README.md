# GitHub Activity Monitor

GitHub Activity Monitor allows you to monitor the activity on your GitHub repositories based on the Github Events API (https://api.github.com/events) and gain insights into the contributions, issues, and pull requests. The documentation of the Github Events API can be found [here](https://docs.github.com/en/rest/activity/events). The application is built using Python and [Litestar](https://litestar.dev/) and can be split into three parts:
- Ingestor `./ingestor`: The ingestor is a Python application that polls the GitHub Events API and stores the data in a (PostgreSQL) database.
- Database: A (PostgreSQL) database that stores the data from the GitHub Events API.
- API `./api`: The API is a Python application using Litestar that provides endpoints to query the data from the database.


## System Context diagram

The diagram describes a high level system context of the GitHub Activity Monitor.

![C1](drawio/github-activity-monitor.drawio.svg)

## Requirements
| Name | Version |
|-|-|
| Docker Engine | >=20.10.13 |
| Docker Compose | >=1.29.2 |


## Environment Variables

### Required
None

### Optional

`GITHUB_TOKEN` - GitHub API token, which allows the ingestor to increase the API call limit 60 to 5000 requests per hour. Documentation for generating the token can be found [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).
`MAX_POLL_INTERVAL` - Maximum interval in seconds in which the GitHub Events API is polled. Default: `10`


In case you want to run the ingestor and API separately, you need additional environment variables to connect to a (PostgreSQL) database. Please view the READMEs in the respective folders.


## Run Locally

Although the ingestion and API can be run separately, the easiest way to run everything together is using docker-compose. This will start the ingestor, database and API in separate containers and link them together. Make sure that ports 5432 and 8000 are not in use.

```bash
  docker compose up
```

Check out the OpenAPI-based documentation at:
- http://localhost:8000/schema (for ReDoc)
- http://localhost:8000/schema/swagger (for Swagger UI)
- http://localhost:8000/schema/elements (for Stoplight Elements)

To run the `ingestor` and `api` separately, please view the READMEs in the respective folders.

## CI/CD

The CI/CD pipeline is implemented using GitHub Actions. The workflows can be found in `.github/workflows`. The pipeline is triggered on every push to the `main` branch and runs the following steps for the `ingestor` and `api` repository respectively:
- Linting of Python code using [flake8](https://flake8.pycqa.org/en/latest/)
- Run unit tests using [pytest](https://docs.pytest.org/en/6.2.x/)

## Deployment
TO BE DONE
