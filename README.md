### Description

- Github Actions self hosted runner as docker-compose without interactive input
- With docker in docker available (docker-compose) to self hosted runner jobs :)

### Commands

- `TOKEN=your_github_token docker-compose up` in order to run it. Optionally add `-d` in order to run in background.
- `TOKEN_ORG=org_api_token ORG=org_name docker-compose up` for self registry in organization
- `docker-compose down --volume` to destroy configured runner

### requirements:

having installed docker-compose and running docker daemon

### Docker hub

- https://hub.docker.com/repository/docker/darkwind8/github_runner
- see example to run in docker-compose.hub.yml