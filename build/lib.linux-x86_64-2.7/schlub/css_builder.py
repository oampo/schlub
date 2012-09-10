from __future__ import print_function

import subprocess

import schlub.util

class CSSBuilder:
    def build(self):
        fileNames = schlub.util.findFiles("less", "*.less", 1)
        for fileName in fileNames:
            command = ["lessc", "--include-path=less/include", fileName]
            output = subprocess.check_output(command)
            key = schlub.util.fileNameToKey(fileName)
            outputFileName = "css/{}.css".format(key)
            schlub.util.writeWithCreate(outputFileName, output.decode("utf-8"))

