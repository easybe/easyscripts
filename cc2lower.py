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
        self._history = {}

        parser = optparse.OptionParser(add_help_option=True)
        parser.add_option("-l", "--load-hist", dest="loadFilenames", action="append",
                          help="a history file which will be used")
        parser.add_option("-i", "--ignore-file", dest="ignoreFilenames", action="append",
                          help="file with names to ignore")
        parser.add_option("-d", "--dump-hist", dest="dumpFilename",
                          help="file to dump history to")
        parser.add_option("-a", "--all-files", dest="all", action="store_true",
                          help="process all files")

        self._options, args = parser.parse_args(argv)

    def run(self):

        self._loadHistory()

        d = os.getcwd()

        paths = []
        for root, dirnames, filenames in os.walk(d):
            for name in filenames:
                paths.append(os.path.join(root, name))

        answ = ''
        for path in paths:
            if not self._options.all:
                answ = raw_input("Edit {0} ?\n(y, n, q) [y]: ".format(path))

            if not answ:
                answ = 'y'

            if answ == 'q':
                break
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
                    if name.startswith("0x"):
                        continue
                    if name in self._history:
                        newName = self._history[name]
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
                        self._history[name] = newName
                        line = line.replace(name, newName)
                    else:
                        self._history[name] = name

                newFile.write(line)
                lineNumber += 1

            newFile.close()
            os.close(fhTmp)
            oldFile.close()
            mode = os.stat(path).st_mode & 0777
            os.chmod(pathTmp, mode)
            # Remove original file
            os.remove(path)
            # Move new file
            shutil.move(pathTmp, path)

        if self._options.dumpFilename:
            self._dumpHistory()

        print "bye"

    def _loadHistory(self):
        if self._options.loadFilenames is not None:
            for filename in self._options.loadFilenames:
                histFile = open(filename, 'r')
                for line in histFile:
                    (key, _, val) = line.rstrip('\n').partition(':')
                    if val:
                        self._history[key] = val
                histFile.close()

        if self._options.ignoreFilenames is not None:
            for filename in self._options.ignoreFilenames:
                ignoreFile = open(filename, 'r')
                for line in ignoreFile:
                    name = line.rstrip('\n')
                    if name:
                        self._history[name] = name
                ignoreFile.close()

    def _dumpHistory(self):
        dumpFile = open(self._options.dumpFilename, 'w')

        for k, v in sorted(self._history.iteritems()):
            dumpFile.write(k + ':' + v + '\n')

    def _convert(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

if __name__ == "__main__":
    main = Main()
    sys.exit(main.run())
