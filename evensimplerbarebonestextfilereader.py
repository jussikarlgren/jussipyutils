import json
import csv
import re
import os
from math import log

from logger import logger

error = True
verbose = False
debug = False
monitor = True

stats = None

filterterms = None

urlpatternexpression = re.compile(r"https?://[/A-Za-z0-9\.\-\?_]+", re.IGNORECASE)
handlepattern = re.compile(r"@[A-Za-z0-9_\-±.]+", re.IGNORECASE)


def getfilelist(resourcedirectory:str="/home/jussi/data/storm/fixed", patternstring:str=r".*irma"):
    pattern = re.compile(patternstring)
    filenamelist = []
    for filenamecandidate in os.listdir(resourcedirectory):
        if pattern.match(filenamecandidate):
            logger(filenamecandidate, debug)
            filenamelist.append(os.path.join(resourcedirectory,filenamecandidate))
    logger(filenamelist, debug)
    return sorted(filenamelist)


def readtexts(json=True) -> list:
    '''Read a set of files and return sentences found in them.'''
    filenamelist = getfilelist()
    if json:
        sentences = dojsontextfiles(filenamelist, debug)
    else:
        sentences = []
        for f in filenamelist:
            ss = doonerawtextfile()
            sentences = sentences + ss
    return sentences



def doonerawtextfile(filename, loglevel=False):
    '''Read one file with texts, one per line.'''
    logger(filename, loglevel)
    sentencelist = []
    with open(filename, errors="replace", encoding='utf-8') as inputtextfile:
        logger("Loading " + filename, loglevel)
        for textline in inputtextfile:
            sents = textline.replace("!", ".").replace("?", ".").replace(",", "").rstrip("\n").lstrip().split(".")
            for sentence in sents:
                logger(sentence, debug)
                sentencelist = sentencelist + sents
    return sentencelist

