#!/usr/bin/env python
"""Episode Rename

Batch renames TV episodes

easyb
"""

import sys
import re
import os
import optparse
import tvdb_api


class Main(object):
    def __init__(self, argv = None):
        usage = "usage: %prog [options] [name of show]"
        parser = optparse.OptionParser(usage=usage)
        parser.add_option("-d", "--dry-run",
                          dest="dry",
                          default=False,
                          action="store_true",
                          )
        parser.add_option("-p", "--path",
                          dest="path",
                          metavar="DIRECTORY"
                          )

        options, remainder = parser.parse_args()
        self._dry = options.dry
        self._season_no = None

        if options.path:
            self._path = unicode(os.path.abspath(options.path))
        else:
            self._path = os.getcwdu()

        if remainder:
            self._search_str = " ".join(remainder)
        elif self._path:
            info = self._get_info_from_path()
            if info:
                self._search_str = info[0]
                self._season_no = info[1]
            else:
                parser.print_help()
                self._exit("")

        if self._dry:
            print "*** Dry run requested ***"

        self._tvdb = tvdb_api.Tvdb()

    def run(self):
        results = self._tvdb.search(self._search_str)
        if len(results) == 0:
            self._exit("Could not find requested show")
        show_name = results[0]['seriesname']
        answ = 'n'
        if self._season_no is not None:
            answ = self._prompt("Rename '{0}' season {1:d} ?".format(
                show_name, self._season_no), 'y')

        while answ != 'y':
            i = 0
            for result in results:
                name = result['seriesname']
                print u"[{0:d}] {1}".format(i, name)
                i += 1
            print "[q] Never mind..."
            show_index = self._prompt_for_number("Select a show")
            choice = results[show_index]
            show_name = choice['seriesname']
            latest_season = self._tvdb[show_name].keys()[-1]
            self._season_no = self._prompt_for_number(
                "Select a season", latest_season)
            answ = self._prompt("Rename '{0}' season {1:d} ?".format(
                show_name, self._season_no), 'y')

        self._show_name = show_name

        self._fetch_episode_names()
        self._rename()

    def _fetch_episode_names(self):
        self._names = dict()
        for episode_no, episode in self._tvdb[
                self._show_name][self._season_no].items():
            number_str = "{0:d}{1:02d}".format(self._season_no, episode_no)
            title = episode['episodename']
            if not title:
                continue
            title = re.sub('/', '-', title)
            self._names[number_str] = number_str + " - " + title

    def _rename(self):
        os.chdir(self._path)
        files = os.listdir(os.getcwdu())
        for file in files:
            m = re.search('[Ss](\d+)[Ee](\d+)', file)
            if not m:
                m = re.search('(\d+)[Xx](\d+)', file)
            if not m:
                m = re.search('^(\d+)(\d{2})', file)
            if not m:
                m = re.search('\.(\d+)(\d{2})\.', file)
            if not m:
                m = re.search('(?:Season|Series) (\d+).*Episode (\d+)', file)
            if m:
                key = "{0:d}{1:02d}".format(int(m.group(1)), int(m.group(2)))
                ext = re.search('(\.\w*)$', file).group(1)

                if key in self._names:
                    name = self._names[key] + ext
                    if file != name:
                        print u"renaming '{0}' to '{1}'".format(file, name)
                        if not self._dry: os.rename(file, name)

    def _get_info_from_path(self):
        d = os.path.basename(self._path)
        m = re.search('(.*) - Season (\d*)', d)
        if m:
            return (m.group(1), int(m.group(2)))

        return None

    def _prompt_for_number(self, msg, default='0'):
        answ = ''
        while not answ.isdigit():
            answ = self._prompt(msg, default)

        return int(answ)

    def _prompt(self, msg, default='y'):
        answ = raw_input("{0} [{1}]: ".format(msg, default))
        if answ == 'q':
            self._exit("bye")
        if not answ:
            answ = default
        answ = answ.strip()

        return answ

    def _exit(self, msg):
        print msg
        quit()

if __name__ == "__main__":
    main = Main()
    sys.exit(main.run())
