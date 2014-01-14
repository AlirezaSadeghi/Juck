#!/usr/bin/env python
from os.path import dirname, abspath
import os
import sys


sys.path.insert(0, dirname(dirname(abspath(__file__))))
<<<<<<< HEAD
sys.path.insert(1, '/home/alireza/Documents/Juck/lib')
=======
sys.path.insert(1, '/Users/Aref/Sites/juck/lib')
>>>>>>> 8a50be88bb48b0d1df8eb15874971fc522c4944b


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "juck.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

