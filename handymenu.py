#!/usr/bin/python
# -*- coding:Utf-8 -*- 

import sys
from lib.handymenu_app import *

if __name__ == "__main__":
    arg = "prof"
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    if arg not in ["prof", "mini", "super", "maxi"]:
        print('Impossible de lancer un applificatif qui n\'est ni "prof" ni "mini", ni "super", ni "maxi')
        exit(0)
    main(arg)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
