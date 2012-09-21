#!/usr/bin/env python

"""Interactive CamleCase to lower_case conversion

easyb 2012
"""

import os
import re
import sys
import tempfile
import shutil
import optparse

class Main(object):
    def __init__(self, argv = None):
        self.history = {}

        parser = optparse.OptionParser()
        parser.add_option("-i", "--ignore-file", dest="ignoreFilenames", action="append",
                          help="file with names to ignore")

        options, args = parser.parse_args(argv)

        names = []

        for filename in options.ignoreFilenames:
            ignoreFile = open(filename, 'r')
            for line in ignoreFile:
                names += filter(None, re.findall('(\w*[a-z][A-Z]\w*)*', line))

            #print len(names)

            # Remove duplicates
            d = {}
            for n in names:
                d[n] = 1
            names = list(d.keys())

            for name in names:
                self.history[name] = name

    def run(self):

        d = os.getcwd()

        paths = []
        for root, dirnames, filenames in os.walk(d):
            for name in filenames:
                paths.append(os.path.join(root, name))

        for path in paths:
            answ = raw_input("Edit {0} ?\n(y, n, q) [y]: ".format(path))
            if not answ:
                answ = 'y'

            if answ == 'q':
                quit()
            elif answ != 'y':
                continue

            oldFile = open(path, 'r')
            # Create temp file
            fhTmp, pathTmp = tempfile.mkstemp()
            newFile = open(pathTmp, 'w')

            lineNumber = 1
            for line in oldFile:
                names = filter(None, re.findall('(\w*[a-z][A-Z]\w*)*', line))

                for name in names:
                    if name in self.history:
                        newName = self.history[name]
                        answ = 'y'
                    else:
                        newName = self._convert(name)
                        answ = ''
                        while not (answ == 'y' or answ == 'n'):
                            answ = raw_input(
                                "Replace {0} with {1} (y, n, e, l) [y]: "
                                .format(name, newName))

                            if answ == 'e':
                                tmpName = newName
                                tmpName = raw_input(
                                    "Enter the new name [{0}]: "
                                    .format(newName))
                                if tmpName:
                                    newName = tmpName
                                answ = 'y'
                            elif answ == 'l':
                                print "{0}: {1}".format(lineNumber, line)

                            elif not answ:
                                answ = 'y'

                    if answ == 'y':
                        self.history[name] = newName
                        line = line.replace(name, newName)
                    else:
                        self.history[name] = name

                newFile.write(line)
                lineNumber += 1

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
