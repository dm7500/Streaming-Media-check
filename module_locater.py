#-------------------------------------------------------------------------------
# Name:        module_locater
# Purpose:     Marker to find file location in other scripts. Call module_path()
#               to list path.
#
# Author:      David.Martinez@duffandphelps.com
#
# Created:     04/23/2014
# Copyright:   (c) Duff&Phelps 2014
#-------------------------------------------------------------------------------

import sys, os

def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))