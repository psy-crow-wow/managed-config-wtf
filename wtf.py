#!/usr/bin/env python3
from collections import OrderedDict
import argparse
import os
import re
import shutil
import sys
import yaml

parser = argparse.ArgumentParser(description="Set Config.wtf CVars")
parser.add_argument(
    "wtf_dir", nargs=1, type=str, default="C:\Program Files (x86)\World of Warcraft\WTF"
)
args = parser.parse_args()
wtf_dir = args.wtf_dir[0]
if not os.path.isdir(wtf_dir):
    print(f"{wtf_dir} is not a directory", file=sys.stderr)
    sys.exit(1)


re_wtf_cvar = re.compile(r'^SET (?P<key>[^ ]*) "(?P<value>[^"]*)"$')
re_config_wtf = re.compile(r"(?i)^config.*\.wtf$")

cvars = OrderedDict()
managed_cvars = {}

with open("managed_cvars.yaml") as f:
    data = yaml.safe_load(f)
    managed_cvars = data["managed_cvars"]

for file in os.listdir(wtf_dir):
    if re_config_wtf.match(file):
        config_wtf = os.path.join(wtf_dir, file)
        shutil.copy(config_wtf, f"{config_wtf}.bak")

        with open(config_wtf, "r") as f:
            for line in f.readlines():
                m = re_wtf_cvar.match(line.strip())
                if m is not None:
                    cvars[m["key"]] = m["value"]

        for k, v in managed_cvars.items():
            cvars[k] = v

        lines = []
        for k, v in cvars.items():
            lines += [f'SET {k} "{v}"']

        with open(config_wtf, "w") as f:
            f.write(f"{os.linesep}".join(lines))
