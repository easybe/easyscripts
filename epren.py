#!/usr/bin/env python

import os
import urllib2
from xml.dom import minidom

def getVal(node, tag):
    return node.getElementsByTagName(tag)[0].firstChild.nodeValue

def parseUrl(url):
    return minidom.parse(urllib2.urlopen(url))

infoUrl = "http://www.tvrage.com/feeds/search.php?show="
epUrl = "http://www.tvrage.com/feeds/episode_list.php?sid="

query = "friends"
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

seasons = xmlDoc.getElementsByTagName("Season")
for season in seasons:
    if season.hasAttribute("no"):
        no = season.getAttribute("no")
        if no == seasonNo:
            print "found"
            break;
            
episodes = season.getElementsByTagName("episode")

newNames = dict()
for episode in episodes:
    epNum = int(getVal(episode, "seasonnum"))
    numberStr = "{0:d}{1:02d}".format(seasonNo, epNum)
    title = getVal(episode, "title")
    filename = numberStr + " - " + title
    newNames[numberStr] = filename

#import pdb; pdb.set_trace()

currentDir = os.getcwd()

files = os.listdir(currentDir)
for file in files:
    print file



