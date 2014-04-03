#! /usr/bin/env python
import os, sys

def removeEmptyFolders(path):
  if not os.path.isdir(path):
    return

  # remove empty subfolders
  files = os.listdir(path)
  if len(files):
    for f in files:
      fullpath = os.path.join(path, f)
      if os.path.isdir(fullpath):
        removeEmptyFolders(fullpath)

  # if folder empty, delete it
  files = os.listdir(path)
  if len(files) == 0:
    print "Removing empty folder:", path
    os.rmdir(path)

removeEmptyFolders(sys.argv[1])