#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

def obtain_console_input():
  while True:
    _input = raw_input("""
      Give me a string to validate some tokens.
      Valid tokens look like: Abc@1,2w3E*
      Invalid tokens look like: abc@1,2w3:

""")
    if _input:
      return _input

class ValidationError(Exception):
  pass

PASSWORD_CLASS_TYPES = {
  'a-z': re.compile("(?:[a-z])"),
  'A-Z': re.compile("(?:[A-Z])"),
  '0-9': re.compile("(?:[0-9])"),
  'special': re.compile("(?:[*#+@])"),
}
def password_match_types(value):
  for key, regex in PASSWORD_CLASS_TYPES.iteritems():
    if not regex.search(value):
      raise ValidationError("Match not found: %s" % key)

def validate_for_zero_spaces(value):
  if len(re.split(r'\s', value)) > 1:
    raise ValidationError("Spaces are not allowed.")

def validate_min_len(value, num=4):
  if len(value) < num:
    raise ValidationError("Min amount not meet. %d" % num)

def validate_max_len(value, num=6):
  if len(value) > num:
    raise ValidationError("Max amount not meet. %d" % num)

def validate_sequence(passwords):
  passed = []
  for pw in passwords.split(','):
    try:
      password_match_types(pw)
      validate_for_zero_spaces(pw)
      # min-check is kind of redundent with the PASSWORD_CLASS_TYPE alg I have going on
      validate_min_len(pw, 4)
      validate_max_len(pw, 6)
      passed.append(pw)
    except ValidationError:
      pass

  return passed

if __name__ == '__main__':
  # Input
  # Abc@1,a B1#,2w3E*,2We#3345
  # Expected Result
  # Abc@1,2w3E*

  _input = obtain_console_input()
  print "These tokens are valid:"
  print ','.join(validate_sequence(_input))
