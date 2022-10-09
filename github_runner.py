print("starting to run.py")

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
parser.add_argument(
    '--token',
    type=str,
    dest='token',
    help='Github token',
    default=os.environ["TOKEN"],
    )

args = parser.parse_args()
print("starting to parsed args")

print("trying to configure")
subprocess.run(f'./config.sh --url {args.url} --token {args.token}', shell=True)

print("python3: running listener")
subprocess.run("./run.sh", shell=True, check=True)

