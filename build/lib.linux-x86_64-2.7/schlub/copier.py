from __future__ import print_function

import os
import os.path
import shutil
import distutils.dir_util

class Copier:
    def __init__(self):
        self.assets = ["css", "js", "images", "audio", "video", "fonts"]
    def copy(self):
        for item in self.assets:
            if os.path.isdir(item):
                path = os.path.join("assets/assets", item)
                distutils.dir_util.copy_tree(item, path)
            elif os.path.isfile(item):
                shutil.copy(item, "assets/assets")
                
