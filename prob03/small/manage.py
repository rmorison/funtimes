#!/usr/bin/env python
import os
import sys
print """
Yeah, I'm trying to look my best here...expect my code qualty to go
    up and down respectivly with the task at hand.
"""
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "small.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
