# Description

Github Actions self hosted runner as docker-compose without interactive input
With side car container with docker in docker available to self hosted runner :)

- `TOKEN=your_github_token docker-compose up` in order to run it. Optionally add `-d` in order to run in background.
- `docker-compose down --volume` to destroy configured runner

## requirements:

having installed docker-compose and running docker daemon