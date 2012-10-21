#!/usr/bin/env python

import glob
import re

txt = ''
for fn in glob.glob('*_*.tex'):
    with open(fn, 'r') as f:
        txt += f.read()

txt = txt.lower()
m = re.findall(r'(\w+)-(\w+)', txt)
bad = []
for words in m:
    if ''.join(words) in txt:
        bad.append(words)

print '\n'.join(sorted(map(str, set(bad))))
