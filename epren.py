#!/usr/bin/env python

"""Episode Rename

Renames TV episode with a little help of tvrage.com

easyb 2012
"""

import sys
import re
import os
import urllib2
import optparse
from xml.dom import minidom


class Main(object):

    def __init__(self, argv = None):

        usage = "usage: %prog [options] keyword"
        parser = optparse.OptionParser(usage=usage)
        parser.add_option("-d", "--dry-run",
                          dest="dry",
                          default=False,
                          action="store_true",
                          )

        options, remainder = parser.parse_args()
        self._dry = options.dry
        if remainder:
            self._searchStr = remainder[0]
        else:
            parser.print_help()
            self._exit("")

        if self._dry:
            print "*** Dry run requested ***"

    def run(self):
        self._fetchNames()

        currentDir = os.getcwd()

        files = os.listdir(currentDir)
        for file in files:
            m = re.search('S0?(\d)[Ee](\d{2})', file)
            if not m:
                 m = re.search('0?(\d)x(\d{2})', file)
            if m:
                key = m.group(1) + m.group(2)
                ext = re.search('(\..*)$', file).group(1)

                if self._names.has_key(key):
                    name = self._names[key] + ext
                    print "renaming '{0:s}' to '{1:s}'".format(file, name)
                    if not self._dry: os.rename(file, name)

    def _fetchNames(self):

        infoUrl = "http://www.tvrage.com/feeds/search.php?show="
        epUrl = "http://www.tvrage.com/feeds/episode_list.php?sid="

        xmlDoc = self._parseUrl(infoUrl + self._searchStr)
        shows = xmlDoc.getElementsByTagName("show")
        if len(shows) == 0:
            self._exit("Could not find requested show")

        i = 0
        for show in shows:
            name = self._getVal(show, "name")
            print "[{0:d}] {1:s}".format(i, name)
            i += 1

        index = self._requestNumber("Select a show")

        show = shows[index]
        name = self._getVal(show, "name")
        showId = self._getVal(show, "showid")
        seasonCount = self._getVal(show, "seasons")

        print "You have selected: " + name

        seasonNo =  self._requestNumber("Select an season", seasonCount)

        xmlDoc = self._parseUrl(epUrl + showId)

        seasons = xmlDoc.getElementsByTagName("Season")
        if len(seasons) == 0:
            self._exit("No seasons found")

        for season in seasons:
            if season.hasAttribute("no"):
                no = season.getAttribute("no")
                if no == seasonNo:
                    break;

        episodes = season.getElementsByTagName("episode")

        self._names = dict()
        for episode in episodes:
            epNum = int(self._getVal(episode, "seasonnum"))
            numberStr = "{0:d}{1:02d}".format(seasonNo, epNum)
            title = self._getVal(episode, "title")
            filename = numberStr + " - " + title
            self._names[numberStr] = filename

    def _requestNumber(self, msg, default="0"):
        answ = ""
        while not answ.isdigit():
            answ = raw_input("{0:s} [{1:s}]: ".format(msg, default))
            if answ == "q":
                self._exit("bye")
            if not answ:
                answ = default
        answ = answ.strip()

        return int(answ)

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
