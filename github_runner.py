print("starting to run.py")

import requests
import argparse
import os
import subprocess
from dataclasses import dataclass

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

@dataclass
class GithubRunnerArgs:
    url: str
    token: str

class GithubRunner:

    def __init__(self, args: GithubRunnerArgs = None):
        if args is not None:
            self.args = args
            return

        print("starting to parse args")
        args = parser.parse_args()

        token = args.token

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

            token = data["token"]
        
        self.params = GithubRunnerArgs(url=args.url, token=token)

    def run(self):
        try:
            print("trying to configure")
            subprocess.run(f"runuser -l user -c 'cd /app && ./config.sh --labels upptime --url {self.params.url} --token {self.params.token}'", shell=True)
            print("python3: running dockerd")
            subprocess.Popen("dockerd", shell=True)
            print("running main proc")
            subprocess.run(f"runuser -l user -c 'cd /app && ./run.sh'", shell=True, check=True)
            # in case of reload from update
            subprocess.run(f"runuser -l user -c 'cd /app && ./run.sh'", shell=True, check=True)
        finally:
            self._shutdown()

    def _shutdown(self):
        subprocess.run(f"runuser -l user -c 'cd /app && ./config.sh remove --token {self.params.token}'", shell=True)    
        print("End of the program. I was killed gracefully :)")

def main():
    runner = GithubRunner()
    runner.run()

if __name__=="__main__":
    main()
