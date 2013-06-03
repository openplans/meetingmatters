#!/usr/bin/env python
import os, sys

ROOT = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(ROOT)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)