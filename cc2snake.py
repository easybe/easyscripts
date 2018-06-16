#!/usr/bin/env python

"""Interactive CamleCase to lower_case conversion

easyb 2012-2014
"""

import os
import re
import sys
import tempfile
import shutil
import optparse


class Main(object):
    def __init__(self, argv=None):
        self._history = {}

        parser = optparse.OptionParser(add_help_option=True)
        parser.add_option("-l", "--load-hist", dest="load_filenames",
                          action="append",
                          help="a history file which will be used")
        parser.add_option("-i", "--ignore-file", dest="ignore_filenames",
                          action="append",
                          help="file with names to ignore")
        parser.add_option("-d", "--dump-hist", dest="dump_filename",
                          help="file to dump history to")
        parser.add_option("-a", "--all-files", dest="all", action="store_true",
                          help="process all files")
        parser.add_option("-f", "--files", dest="files", action="append",
                          help="files to process")
        parser.add_option("-p", "--python-mode", dest="python_mode",
                          action="store_true",
                          help="proccess Python files according to PEP 8")

        self._options, args = parser.parse_args(argv)

    def run(self):
        self._load_history()

        paths = []

        if self._options.files:
            paths += self._options.files
        else:
            cwd = os.getcwd()
            for root, dirnames, filenames in os.walk(cwd):
                filenames = [f for f in filenames if not f[0] == '.']
                dirnames[:] = [d for d in dirnames if not d[0] == '.']

                for name in filenames:
                    paths.append(os.path.join(root, name))

        answ = ''
        for path in paths:
            file_name = os.path.basename(path)
            if re.search(r'^[\.#_]', file_name):
                continue

            if re.search(r'^\w+$|(\.(sh|py|cpp|hpp|c|h|)$)',
                         file_name) is None:
                continue

            if not self._options.all:
                answ = raw_input("Edit {0} ?\n(y, n, q) [y]: ".format(path))

            if not answ:
                answ = 'y'

            if answ == 'q':
                break
            elif answ != 'y':
                continue

            old_file = open(path, 'r')
            # Create temp file
            fh_tmp, path_tmp = tempfile.mkstemp()
            new_file = open(path_tmp, 'w')

            line_number = 1
            for line in old_file:
                names = filter(None, re.findall('(\w*[a-z][A-Z]\w*)*', line))

                for name in names:
                    if name.startswith("0x"):
                        continue
                    if self._options.python_mode and name[0].isupper():
                        continue
                    if name in self._history:
                        new_name = self._history[name]
                        answ = 'y'
                    else:
                        new_name = self._convert(name)
                        answ = ''
                        while not (answ == 'y' or answ == 'n'):
                            print "{0}: {1}".format(line_number, line)
                            answ = raw_input(
                                "Replace {0} with {1} (y, n, e, l) [y]: "
                                .format(name, new_name))

                            if answ == 'e':
                                tmp_name = new_name
                                tmp_name = raw_input(
                                    "Enter the new name [{0}]: "
                                    .format(new_name))
                                if tmp_name:
                                    new_name = tmp_name
                                answ = 'y'

                            elif not answ:
                                answ = 'y'

                    if answ == 'y':
                        self._history[name] = new_name
                        line = line.replace(name, new_name)
                    else:
                        self._history[name] = name

                new_file.write(line)
                line_number += 1

            new_file.close()
            os.close(fh_tmp)
            old_file.close()
            mode = os.stat(path).st_mode & 0777
            os.chmod(path_tmp, mode)
            # Remove original file
            os.remove(path)
            # Move new file
            shutil.move(path_tmp, path)

        if self._options.dump_filename:
            self._dump_history()

        print "done"

    def _load_history(self):
        if self._options.load_filenames is not None:
            for filename in self._options.load_filenames:
                hist_file = open(filename, 'r')
                for line in hist_file:
                    (key, _, val) = line.rstrip('\n').partition(':')
                    if val:
                        self._history[key] = val
                hist_file.close()

        if self._options.ignore_filenames is not None:
            for filename in self._options.ignore_filenames:
                ignore_file = open(filename, 'r')
                for line in ignore_file:
                    name = line.rstrip('\n')
                    if name:
                        self._history[name] = name
                ignore_file.close()

    def _dump_history(self):
        dump_file = open(self._options.dump_filename, 'w')

        for k, v in sorted(self._history.iteritems()):
            dump_file.write(k + ':' + v + '\n')

    def _convert(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


if __name__ == "__main__":
    main = Main()
    sys.exit(main.run())
