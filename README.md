### Description

- Github Actions self hosted runner as docker-compose without interactive input for organization registration

### Commands

- `ORG_URL=https://github.com/${YOURORG} ORG_NAME=${YOUR_ORG} ORG_TOKEN=${YOUR_TOKEN} docker run -it --privileged darkwind8/github_runner:org-latest`

### Requirements:

having installed docker-compose and running docker daemon

### Docker hub

- https://hub.docker.com/repository/docker/darkwind8/github_runner
- see example to run in docker-compose.hub.yml