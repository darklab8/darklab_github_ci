print("starting to run.py")

import argparse
import pexpect
import os
import sys
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

child = pexpect.spawn(
    f'./config.sh --url {args.url} --token {args.token}',
    encoding='utf-8',
    logfile=sys.stdout,
)
print("lanched process")
child.expect('the name of the runner group') # Default
child.sendline("\n")
child.expect('name of runner') # random ID
child.sendline("\n")
child.expect('Enter any additional labels')
child.sendline("\n")
child.expect('name of work folder') # _work
child.sendline("\n")

subprocess.run("./run.sh", shell=True, check=True)