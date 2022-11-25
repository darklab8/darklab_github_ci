FROM ubuntu:20.04

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
RUN curl -o actions-runner-linux-x64-2.294.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.294.0/actions-runner-linux-x64-2.294.0.tar.gz
RUN tar xzf ./actions-runner-linux-x64-2.294.0.tar.gz

RUN apt install -y python3-pip
RUN pip install requests

COPY ./github_runner.py ./

RUN chmod a=rwx -R /app
# only non root user can launch it
RUN adduser --disabled-password --gecos "" user
RUN chown -R user /app
WORKDIR /code
RUN chmod a=rwx -R /code
RUN chown -R user /code

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

CMD rm -r /code/* ; cp -a /app/. /code/ && python3 /code/github_runner.py
