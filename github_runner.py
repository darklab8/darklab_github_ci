print("starting to run.py")

import requests
import argparse
import os
import subprocess

print("inited libs")
parser = argparse.ArgumentParser()
parser.add_argument(
    '--url',
    type=str,
    dest='url',
    help='To which Github project/group is added',
    default=os.environ.get("URL", "https://github.com/darklab8"),
    )

# Get Token Runner
# https://docs.github.com/en/rest/actions/self-hosted-runners#create-a-registration-token-for-an-organization

import os
print(os.environ)
parser.add_argument(
    '--token-org',
    type=str,
    dest='token_org',
    help='Github Organization API token, scope=admin:org is required',
    default=os.environ.get("TOKEN_ORG"),
    )
parser.add_argument(
    '--org',
    type=str,
    dest='org',
    help='Org namespace',
    default=os.environ.get("ORG"),
    )

# Left for legacy backward compatibility
parser.add_argument(
    '--token',
    type=str,
    dest='token',
    help='Github Runner Registry Token',
    default=os.environ.get("TOKEN"),
)

args = parser.parse_args()

token = args.token

print(f"{args.token_org=}")
if args.token_org:
    response = requests.post(
        url=f"https://api.github.com/orgs/{args.org}/actions/runners/registration-token",
        headers=dict(
            Accept="application/vnd.github+json",
            Authorization=f"Bearer {args.token_org}",
        ),
    )
    data = response.json()
    print("queried REST API for token")
    print(data)

    token = data["token"]

print("starting to parsed args")

print("trying to configure")
subprocess.run(f"runuser -l user -c 'cd /code && ./config.sh --url {args.url} --token {token}'", shell=True)

print("python3: running listener")
subprocess.run("runuser -l user -c 'cd /code && ./run.sh'", shell=True, check=True)

