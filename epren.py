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
        self._seasonNo = None

        if options.path:
            self._path = os.path.abspath(options.path)
        else:
            self._path = os.getcwd()

        if remainder:
            self._searchStr = urllib.quote(" ".join(remainder))
        elif self._path:
            info = self._getInfoFromPath()
            if info:
                self._searchStr = urllib.quote(" ".join(info[0]))
                self._seasonNo = info[1]
            else:
                parser.print_help()
                self._exit("")

        if self._dry:
            print "*** Dry run requested ***"

    def run(self):
        self._fetchShows()
        self._show = self._shows[0]
        showName = self._getVal(self._show, "name")
        answ = 'n'
        if self._seasonNo is not None:
            answ = self._prompt("Rename '{0}' season {1:d} ?".format(
                showName, self._seasonNo), 'y')

        while answ != 'y':
            i = 0
            for show in self._shows:
                name = self._getVal(show, "name")
                print u"[{0:d}] {1}".format(i, name)
                i += 1
            print "[q] Never mind..."

            showIndex = self._promptForNumber("Select a show")
            self._show = self._shows[showIndex]
            showName = self._getVal(self._show, "name")
            seasonCount = self._getVal(self._show, "seasons")
            self._seasonNo = self._promptForNumber(
                "Select a season", str(seasonCount))
            answ = self._prompt("Rename '{0}' season {1:d} ?".format(
                showName, self._seasonNo), 'y')

        self._fetchEpisodeNames()
        self._rename()

    def _fetchShows(self):
        infoUrl = "http://www.tvrage.com/feeds/search.php?show="

        xmlDoc = self._parseUrl(infoUrl + self._searchStr)
        self._shows = xmlDoc.getElementsByTagName("show")
        if len(self._shows) == 0:
            self._exit("Could not find requested show")

    def _fetchEpisodeNames(self):
        epUrl = "http://www.tvrage.com/feeds/episode_list.php?sid="

        showId = self._getVal(self._show, "showid")
        xmlDoc = self._parseUrl(epUrl + showId)

        seasons = xmlDoc.getElementsByTagName("Season")
        if len(seasons) == 0:
            self._exit("No season data available")

        season = None
        for s in seasons:
            if s.hasAttribute("no"):
                if int(s.getAttribute("no")) == self._seasonNo:
                    season = s
                    break;

        if season is not None:
            episodes = season.getElementsByTagName("episode")
        else:
            self._exit("No data for season {0:d} available".format(
                self._seasonNo))

        self._names = dict()
        for episode in episodes:
            epNum = int(self._getVal(episode, "seasonnum"))
            numberStr = "{0:d}{1:02d}".format(self._seasonNo, epNum)
            title = self._getVal(episode, "title")
            title = re.sub('/', '-', title)
            filename = numberStr + " - " + title
            self._names[numberStr] = filename
            
    def _rename(self):
        os.chdir(self._path)
        files = os.listdir(os.getcwd())
        for file in files:
            m = re.search('[Ss](\d+)[Ee](\d+)', file)
            if not m:
                m = re.search('(\d+)x(\d+)', file)
            if not m:
                m = re.search('^(\d+)(\d{2})', file)
            else:
                key = "{0:d}{1:02d}".format(int(m.group(1)), int(m.group(2)))
                ext = re.search('(\.\w*)$', file).group(1)

                if key in self._names:
                    name = self._names[key] + ext
                    if file != name:
                        print u"renaming '{0}' to '{1}'".format(file, name)
                        if not self._dry: os.rename(file, name)

    def _getInfoFromPath(self):
        d = os.path.basename(self._path)
        m = re.search('(.*) - Season (\d*)', d)
        if m:
            return (m.group(1), int(m.group(2)))

        return None

    def _promptForNumber(self, msg, default='0'):
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

    def _getVal(self, node, tag):
        return node.getElementsByTagName(tag)[0].firstChild.nodeValue

    def _parseUrl(self, url):
        return minidom.parse(urllib2.urlopen(url))

    def _exit(self, msg):
        print msg
        quit()

if __name__ == "__main__":
    main = Main()
    sys.exit(main.run())
