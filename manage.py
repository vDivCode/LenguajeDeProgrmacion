#!/usr/bin/env python
# pyrefly: ignore [missing-import]
import os
import sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "career_recommender.settings")
    # pyrefly: ignore [missing-import]
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
