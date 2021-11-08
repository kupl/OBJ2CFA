#!/usr/bin/python
with open('tmp_TunnelingAbstraction.facts', 'r') as f:
    data = [s.strip().split('  ') for s in f.read().splitlines()]

invMth = {}
data2 = [item[0] for item in data]
data2.sort()

for item in data2:
  print (item)


