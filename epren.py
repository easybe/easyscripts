#!/usr/bin/env python
# Requires Python 2.6 or newer

"""Episode Rename

Renames TV episode with a little help of tvrage.com

easyb 2012
"""

import sys
import re
import os
import urllib
import urllib2
import optparse
from xml.dom import minidom


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
            self._search_str = urllib.quote(" ".join(remainder))
        elif self._path:
            info = self._get_info_from_path()
            if info:
                self._search_str = urllib.quote(" ".join(info[0]))
                self._season_no = info[1]
            else:
                parser.print_help()
                self._exit("")

        if self._dry:
            print "*** Dry run requested ***"

    def run(self):
        self._fetch_shows()
        self._show = self._shows[0]
        show_name = self._get_val(self._show, "name")
        answ = 'n'
        if self._season_no is not None:
            answ = self._prompt("Rename '{0}' season {1:d} ?".format(
                show_name, self._season_no), 'y')

        while answ != 'y':
            i = 0
            for show in self._shows:
                name = self._get_val(show, "name")
                print u"[{0:d}] {1}".format(i, name)
                i += 1
            print "[q] Never mind..."

            show_index = self._prompt_for_number("Select a show")
            self._show = self._shows[show_index]
            show_name = self._get_val(self._show, "name")
            season_count = self._get_val(self._show, "seasons")
            self._season_no = self._prompt_for_number(
                "Select a season", str(season_count))
            answ = self._prompt("Rename '{0}' season {1:d} ?".format(
                show_name, self._season_no), 'y')

        self._fetch_episode_names()
        self._rename()

    def _fetch_shows(self):
        info_url = "http://services.tvrage.com/feeds/search.php?show="

        xml_doc = self._parse_url(info_url + self._search_str)
        self._shows = xml_doc.getElementsByTagName("show")
        if len(self._shows) == 0:
            self._exit("Could not find requested show")

    def _fetch_episode_names(self):
        ep_url = "http://services.tvrage.com/feeds/episode_list.php?sid="

        show_id = self._get_val(self._show, "showid")
        xml_doc = self._parse_url(ep_url + show_id)

        seasons = xml_doc.getElementsByTagName("Season")
        if len(seasons) == 0:
            self._exit("No season data available")

        season = None
        for s in seasons:
            if s.hasAttribute("no"):
                if int(s.getAttribute("no")) == self._season_no:
                    season = s
                    break;

        if season is not None:
            episodes = season.getElementsByTagName("episode")
        else:
            self._exit("No data for season {0:d} available".format(
                self._season_no))

        self._names = dict()
        for episode in episodes:
            ep_num = int(self._get_val(episode, "seasonnum"))
            number_str = "{0:d}{1:02d}".format(self._season_no, ep_num)
            title = self._get_val(episode, "title")
            title = re.sub('/', '-', title)
            filename = number_str + " - " + title
            self._names[number_str] = filename

    def _rename(self):
        os.chdir(self._path)
        files = os.listdir(os.getcwdu())
        for file in files:
            m = re.search('[Ss](\d+)[Ee](\d+)', file)
            if not m:
                m = re.search('(\d+)x(\d+)', file)
            if not m:
                m = re.search('^(\d+)(\d{2})', file)
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

    def _get_val(self, node, tag):
        return node.getElementsByTagName(tag)[0].firstChild.nodeValue

    def _parse_url(self, url):
        return minidom.parse(urllib2.urlopen(url))

    def _exit(self, msg):
        print msg
        quit()

if __name__ == "__main__":
    main = Main()
    sys.exit(main.run())
