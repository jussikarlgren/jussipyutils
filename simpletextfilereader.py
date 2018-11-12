import json
import re
import os
from math import log

from logger import logger
from nltk import word_tokenize
from nltk import sent_tokenize

error = True
verbose = False
debug = False
monitor = True

stats = None

filterterms = None

urlpatternexpression = re.compile(r"https?://[/A-Za-z0-9\.\-\?_]+", re.IGNORECASE)
handlepattern = re.compile(r"@[A-Za-z0-9_\-±.]+", re.IGNORECASE)


def getfilelist(resourcedirectory="/home/jussi/data/storm/fixed", pattern=re.compile(r".*irma")):
    filenamelist = []
    for filenamecandidate in os.listdir(resourcedirectory):
        if pattern.match(filenamecandidate):
            logger(filenamecandidate, debug)
            filenamelist.append(os.path.join(resourcedirectory,filenamecandidate))
    logger(filenamelist, debug)
    return sorted(filenamelist)


def readtexts() -> list:
    '''Read a set of files and return sentences found in them.'''
    filenamelist = getfilelist()
    sentences = dojsontextfiles(filenamelist, debug)
    return sentences


def dojsontextfiles(filenamelist1, loglevel=False):
    tweetantal = 0
    sentencelist = []
    filenamelist = sorted(filenamelist1)
    logger("Starting json text file processing ", loglevel)
    logger(str(filenamelist), loglevel)
    for filename in filenamelist:
        sl = doonejsontextfile(filename, loglevel)
        sentencelist = sentencelist + sl
        tweetantal += len(sl)
    return sentencelist


def doonejsontextfile(filename, loglevel=False):
    '''Read one file with a json list of items such as tweets and return the sentences found there.'''
    logger(filename, loglevel)
    sentencelist = []
    with open(filename, errors="replace", encoding='utf-8') as inputtextfile:
        logger("Loading " + filename, loglevel)
        try:
            data = json.load(inputtextfile)
        except json.decoder.JSONDecodeError as e:
            logger("***" + filename + "\t" + str(e.msg), error)
            print(e)
            data = []
        logger("Loaded", loglevel)
        for tw in data:
            try:
                text = tw["rawText"]
                text = urlpatternexpression.sub("URL", text)
                text = handlepattern.sub("HANDLE", text)
                words = word_tokenize(text.lower())
#                if set(words).isdisjoint(filterterms):
#                    continue
                if len(words) > 1 and words[0] == "rt":
                    continue
                else:
                    sents = sent_tokenize(text)
                    for sentence in sents:
                        logger(sentence, debug)
                        sentencelist = sentencelist + sents
            except KeyError:
                if str(tw) != "{}":  # never mind empty strings, no cause for alarm
                    logger("**** " + str(tw) + " " + str(len(sentencelist)), error)
    return sentencelist