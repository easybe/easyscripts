#!/usr/bin/env python

import urllib2
from xml.dom import minidom

def getVal(node, tag):
    return node.getElementsByTagName(tag)[0].firstChild.nodeValue

def parseUrl(url):
    return minidom.parse(urllib2.urlopen(url))

infoUrl = "http://www.tvrage.com/feeds/search.php?show="
epUrl = "http://www.tvrage.com/feeds/episode_list.php?sid="

query = "merlin"
xmlDoc = parseUrl(infoUrl + query)
shows = xmlDoc.getElementsByTagName("show")
i = 0
for show in shows:
    name = getVal(show, "name")
    print "[{0:d}] {1:s}".format(i, name)
    i += 1

index = int(raw_input("Select a show: "))
show = shows[index]
name = getVal(show, "name")
showId = getVal(show, "showid")
seasonCount = getVal(show, "seasons")

print "You have selected: " + name
seasonNo = int(raw_input("Select an episode [1-{0:s}]: ".format(seasonCount)))

xmlDoc = parseUrl(epUrl + showId)

import pdb; pdb.set_trace()