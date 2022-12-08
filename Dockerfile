FROM ubuntu:20.04 as base

WORKDIR /install

# Docker
RUN apt-get update
RUN apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update 
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin 

# Docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose

WORKDIR /app

# installing runner
RUN curl -o action-runner.tar.gz -L https://github.com/actions/runner/releases/download/v2.299.1/actions-runner-linux-x64-2.299.1.tar.gz
RUN tar xzf ./action-runner.tar.gz

RUN chmod a=rwx -R /app
# only non root user can launch it
RUN adduser --disabled-password --gecos "" user
RUN chown -R user /app

RUN apt install -y docker
RUN usermod -aG docker user

RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin
RUN apt-get -y install jq

ENTRYPOINT task org:launch


FROM base as build-org
COPY ./Taskfile.yml ./


# upttime dep https://github.com/upptime/upptime
FROM base as build-org-nodejs-14
RUN curl -sL https://deb.nodesource.com/setup_14.x -o /tmp/nodesource_setup.sh
RUN bash /tmp/nodesource_setup.sh
RUN apt install -y nodejs
COPY ./Taskfile.yml ./