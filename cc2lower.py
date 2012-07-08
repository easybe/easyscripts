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

        for path in paths:
            print "processing " + path

            oldFile = open(path, 'r')
            # Create temp file
            fhTmp, pathTmp = tempfile.mkstemp()
            newFile = open(pathTmp, 'w')

            for line in oldFile:
                names = filter(None, re.findall('(\w*[a-z][A-Z]\w*)*', line))

                for name in names:
                    newName = self._convert(name)
                    answ = raw_input("replace {0} with {1} (y, n, c, q) [y]: "
                        .format(name, newName))
                    if not answ:
                        answ = 'y'
                    if answ == 'y':
                        line = line.replace(name, newName)

                newFile.write(line)

                if answ == 'q' or answ == 'c':
                    break

            newFile.close()
            os.close(fhTmp)
            oldFile.close()
            # Remove original file
            os.remove(path)
            # Move new file
            shutil.move(pathTmp, path)

            if answ == 'q':
                quit()

    def _convert(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

if __name__ == "__main__":
    main = Main()
    sys.exit(main.run())
