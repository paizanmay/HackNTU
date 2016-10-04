# -*- coding: utf-8 -*-
def isEnglish(s):
    try:
        s.decode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True
        