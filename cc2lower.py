#!/usr/bin/env python

"""Interactive CamleCase to lower_case conversion

easyb 2012
"""

import os
import re
import sys
import tempfile
import shutil


class Main(object):
    def __init__(self, argv = None):
        pass

    def run(self):
        d = os.getcwd()

        paths = []
        for root, dirnames, filenames in os.walk(d):
            for name in filenames:
                paths.append(os.path.join(root, name))

        history = dict()

        for path in paths:
            print "Processing " + path

            oldFile = open(path, 'r')
            # Create temp file
            fhTmp, pathTmp = tempfile.mkstemp()
            newFile = open(pathTmp, 'w')

            for line in oldFile:
                names = filter(None, re.findall('(\w*[a-z][A-Z]\w*)*', line))

                for name in names:
                    if name in history:
                        newName = history[name]
                        answ = 'y'
                    else:
                        newName = self._convert(name)
                        answ = ''
                        answ = raw_input(
                            "Replace {0} with {1} (y, n, e) [y]: "
                            .format(name, newName))

                        if answ == 'e':
                            tmpName = ''
                            tmpName = raw_input(
                                "Enter the new name [{0}]: "
                                .format(newName))
                            if tmpName:
                                newName = tmpName
                                answ = 'y'

                        if not answ:
                            answ = 'y'

                    if answ == 'y':
                        history[name] = newName
                        line = line.replace(name, newName)
                    else:
                        history[name] = name

                newFile.write(line)

            newFile.close()
            os.close(fhTmp)
            oldFile.close()
            # Remove original file
            os.remove(path)
            # Move new file
            shutil.move(pathTmp, path)

    def _convert(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

if __name__ == "__main__":
    main = Main()
    sys.exit(main.run())
