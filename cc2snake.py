#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Interactive camleCase to snake_case conversion tool"""

import os
import re
import sys
import json
import tempfile
import shutil
from argparse import ArgumentParser, RawTextHelpFormatter


class Main(object):
    HIST_FILE = ".cc2snake_history"
    FILE_FILTER = r'^\w+$|(\.(sh|py|cpp|hpp|c|h|)$)'

    def __init__(self):
        self._history = {}

        help_text = "By default, every decision you make is recorded and "
        help_text += "applied the next time\nyou run the program from the "
        help_text += "same directory.\n"
        help_text += "The default history file is: ./{}\n"
        help_text += "Remove it to start over or edit it as you please!\n"
        help_text += "To automatically convert all files in tree run: {} -ya"
        help_text = help_text.format(self.HIST_FILE,
                                     os.path.basename(sys.argv[0]))

        parser = ArgumentParser(
            description=help_text, formatter_class=RawTextHelpFormatter)

        parser.add_argument("-l", "--load-hist", dest="load_filenames",
                            action="append",
                            help="history file(s) to load")
        parser.add_argument("-i", "--ignore-file", dest="ignore_filenames",
                            action="append",
                            help="a list of names (one per line) to ignore")
        parser.add_argument("-d", "--dump-hist", dest="dump_filename",
                            help="file to dump history to")
        parser.add_argument("-a", "--all-files", dest="all",
                            action="store_true",
                            help="process all files in tree")
        parser.add_argument("-f", "--files", dest="files",
                            action="append",
                            help="files to process")
        parser.add_argument("-p", "--python-mode", dest="python_mode",
                            action="store_true",
                            help="process Python files according to PEP 8")
        parser.add_argument("-y", "--yes", dest="yes",
                            action="store_true",
                            help="convert everything")
        parser.add_argument("-n", "--no", dest="no",
                            action="store_true",
                            help="don't convert anything (create history file "
                            "for manual editing)")
        parser.add_argument("--file-filter", dest="filter",
                            help="only process files matching (Python) "
                            "regular expression, default:\n    " +
                            self.FILE_FILTER)

        self._args = parser.parse_args()

    def run(self):
        self._load_history()

        paths = []

        if self._args.files:
            paths += self._args.files
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

            file_filter = self.FILE_FILTER
            if self._args.filter is not None:
                file_filter = self._args.filter

            if re.search(file_filter, file_name) is None:
                continue

            if not self._args.all:
                answ = input("Edit {0} ?\n(y, n, q) [y]: ".format(path))

            if not answ:
                answ = 'y'

            if answ == 'q':
                break
            elif answ != 'y':
                continue

            # Determine line endings
            with open(path, 'rU') as f:
                f.readline()
                newline = f.newlines

            # Create temp file by copying to preserve permissions
            fh_tmp, path_tmp = tempfile.mkstemp()
            os.close(fh_tmp)
            shutil.copy(path, path_tmp)

            new_file = open(path_tmp, 'w', newline=newline)
            old_file = open(path, 'rU')

            line_number = 1
            for line in old_file:
                names = filter(None, re.findall('(\w*[a-z0-9][A-Z]\w*)*', line))

                for name in names:
                    if name.startswith("0x"):
                        continue
                    if self._args.python_mode and name[0].isupper():
                        continue
                    if name in self._history:
                        new_name = self._history[name]
                        answ = 'y'
                    else:
                        new_name = re.sub(
                            '([a-z0-9])([A-Z])', r'\1_\2', name).lower()

                        answ = ''
                        if self._args.yes:
                            answ = 'y'
                        elif self._args.no:
                            answ = 'no'

                        while not (answ == 'y' or answ == 'n'):
                            print("\n{0}: {1}".format(line_number, line))
                            answ = input(
                                "Replace {0} with {1} (y, n, e, l) [y]: "
                                .format(name, new_name))

                            if answ == 'e':
                                tmp_name = new_name
                                tmp_name = input(
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
            old_file.close()

            # Remove original file
            os.remove(path)
            # Move new file
            shutil.move(path_tmp, path)

        self._dump_history()

        print("done")

    def _load_history(self):
        filenames = [self.HIST_FILE]
        if self._args.load_filenames is not None:
            filenames = self._args.load_filenames

        for filename in filenames:
            if os.path.isfile(filename):
                with open(filename, 'r') as hist_file:
                    self._history.update(json.load(hist_file))

        if self._args.ignore_filenames is not None:
            for filename in self._args.ignore_filenames:
                ignore_file = open(filename, 'r')
                for line in ignore_file:
                    name = line.rstrip('\n')
                    if name:
                        self._history[name] = name
                ignore_file.close()

    def _dump_history(self):
        dump_filename = self.HIST_FILE
        if self._args.dump_filename is not None:
            dump_filename = self._args.dump_filename

        with open(dump_filename, 'w') as dump_file:
            json.dump(self._history, dump_file, indent=4)


if __name__ == "__main__":
    main = Main()
    sys.exit(main.run())
