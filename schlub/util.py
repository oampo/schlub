from __future__ import print_function

import os
import os.path
import fnmatch
import errno

def findFiles(location, pattern, maxDepth=None):
    matches = []
    for root, dirnames, filenames in os.walk(location):
        if maxDepth and root.count(os.sep) >= maxDepth:
            continue
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches

def writeWithCreate(fileName, data):
    path = os.path.split(fileName)[0]
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
           raise
    with open(fileName, "w") as f:
        f.write(data)

def fileNameToKey(fileName):
    key = os.path.splitext(fileName)[0]
    key = key.split("/")[1:]
    key = os.path.join(*key)
    return key
