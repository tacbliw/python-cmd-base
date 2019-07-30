#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = 'v0.0.1'

#system modules
import os
import sys

"""
SET SCRIPT PATH
"""
WC_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(WC_PATH + '/Modules/')

#wildcat modules
from Modules import wildcat

"""
START SCRIPT
"""
print("\n\x1b[1;37m-------------[ WildCat Commander " + __version__ + " ]----------------")
if __name__ == "__main__":
    try:
        mainProcess = wildcat.Main()
        mainProcess.cmdloop()
    except KeyboardInterrupt:
        print("\nSystem exit!")
        sys.exit()
