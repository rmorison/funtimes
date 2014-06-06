#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def obtain_console_input():
  # Define
  # User Input and validation
  _inputs = []
  idx = 1
  while True:
    _input = raw_input("Give me something to expand[%d of 4]: eg. 2,2 or 2,5\n" % idx)
    if _input:
      try:
        x, y = _input.split(',')
        x = int(x)
        y = int(y)
        _inputs.append([x,y])
        if len(_inputs) > 3:
          break
        idx += 1
      except (IndexError, ValueError), e:
        print "error: Input is not acceptable, use the example to get an idea of what I want"

  return _inputs

if __name__ == '__main__':
  

  # Computation
  def chunk(l,n):
    for i in xrange(0, len(l), n):
      yield l[i:i+n]
  for entry in obtain_console_input():
    result = entry[0] * entry[1]
    print list(chunk(range(1, result+1), entry[1]))

  # import pprint
  # pprint.pprint([bean(i[0]*i[1]) for i in _inputs])
