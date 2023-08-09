# GitHub Activity Monitor

GitHub Activity Monitor allows you to monitor the activity on your GitHub repositories based on the Github Events API (https://api.github.com/events) and gain insights into the contributions, issues, and pull requests. The documentation of the Github Events API can be found [here](https://docs.github.com/en/rest/activity/events). The application is built using Python and [Litestar](https://litestar.dev/).

The GitHub Events API is polled by the ingestor and the data is stored in a PostgreSQL database. The API can be used to query the metrics from the database and return it in a JSON format.

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

In case you want to run the ingestor and API separately, you need additional environment variables to connect to a PostgreSQL database. Please view the READMEs in the respective folders.


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