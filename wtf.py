#!/usr/bin/env python3
import os
import sys
import re
import yaml


r = re.compile('^SET (?P<key>[^ ]*) "(?P<value>[^"]*)"$')

cvars = {}
managed_cvars = {}

with open("managed_cvars.yaml") as f:
    data = yaml.safe_load(f)
    managed_cvars = data["managed_cvars"]

with open(sys.argv[1], "r") as f:
    for line in f.readlines():
        m = r.match(line.strip())
        if m is not None:
            cvars[m["key"]] = m["value"]

for k, v in managed_cvars.items():
    cvars[k] = v

lines = []
for k, v in cvars.items():
    lines += [f'SET {k} "{v}"']

print(f"{os.linesep}".join(lines))
