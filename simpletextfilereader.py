import json
import csv
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


def doonexmltextfile(filename, loglevel=False):
    '''Read one file with a xml struct of items and return the items found there.'''
    logger(filename, loglevel)
    itemlist = []
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


def doonecsvfile(filename, loglevel=False):
    '''Read one file with csv lines such and return the text found in the specified slots.'''
    logger(filename, loglevel)
    sentencelist = []
    with open(filename, errors="replace", newline="", encoding='utf-8') as inputtextfile:
        logger("Loading " + filename, loglevel)
        linereader = csv.reader(inputtextfile, delimiter=',', quotechar='"')
        for line in linereader:
            text = line[3] + " " + line[4]
            illness = line[5]
            id = line[0]
            date = line[2]
            author = line[1]
            text = urlpatternexpression.sub("URL", text)
            text = handlepattern.sub("HANDLE", text)
            words = word_tokenize(text.lower())
            sents = sent_tokenize(text)
            for sentence in sents:
                logger(sentence, debug)
                sentencelist = sentencelist + sents
    return sentencelist


def doonerawtextfile(filename, loglevel=False):
    '''Read one file with texts, one text per line.'''
    logger(filename, loglevel)
    sentencelist = []
    with open(filename, errors="replace", encoding='utf-8') as inputtextfile:
        logger("Loading " + filename, loglevel)
        for textline in inputtextfile:
            #     words = word_tokenize(textline.lower())
            sents = sent_tokenize(textline)
            for sentence in sents:
                logger(sentence, debug)
                sentencelist = sentencelist + sents
    return sentencelist


def doonerawtextfileonmanylines(filename, loglevel=False):
    '''Read one file with texts, join everyting and sentence split it, which can be expensive.'''
    logger(filename, loglevel)
    sentencelist = []
    with open(filename, errors="replace", encoding='utf-8') as inputtextfile:
        logger("Loading " + filename, loglevel)
        txt = ""
        for textline in inputtextfile:
            txt += textline.replace("\n", " ").lstrip()
#                words = word_tokenize(textline.lower())
        sents = sent_tokenize(txt)
        for sentence in sents:
            logger(sentence, debug)
            sentencelist = sentencelist + sents
    return sentencelist


def doonetextfilewithonesentenceperline(filename, loglevel=False):
    '''Read one file with sentences, one per line.'''
    logger(filename, loglevel)
    sentencelist = []
    with open(filename, errors="replace", encoding='utf-8') as inputtextfile:
        logger("Loading " + filename, loglevel)
        for textline in inputtextfile:
            txt = textline.replace("\n", " ").lstrip()
            sentencelist = sentencelist + [txt]
    return sentencelist


def readstats(filename: str = "/home/jussi/data/resources/finfreqcountwoutdigits.list") -> None:
    global stats
    stats = {}
    with open(filename) as statsfile:
        for statsline in statsfile:
            values = statsline.strip().split("\t")
            stats[values[2]] = float(values[1])


def dotweetfiles(datadirectory, filenamelist1, loglevel=False):
    tweetantal = 0
    sentencelist = []
    filenamelist = sorted(filenamelist1)
    logger("Starting tweet file processing ", loglevel)
    logger(str(filenamelist), loglevel)
    for filename in filenamelist:
        sl = doonetweetfile(filename, loglevel)
        sentencelist = sentencelist + sl
        tweetantal += len(sl)


def doonetweetfile(filename, filtersetofstrings:set=None, loglevel=False):
    logger(filename, loglevel)
    date = filename.split(".")[-5].split("/")[-1]
    sentencelist = []
    with open(filename, errors="replace", encoding='utf-8') as tweetfile:
        logger("Loading " + filename, loglevel)
        try:
            data = json.load(tweetfile)
        except json.decoder.JSONDecodeError as e:
            logger("***" + filename + str(e.msg), error)
            data = []
        logger("Loaded", loglevel)
        for tw in data:
            try:
                text = tw["rawText"]
                text = urlpatternexpression.sub("URL", text)
                text = handlepattern.sub("HANDLE", text)
                words = word_tokenize(text.lower())
                if filtersetofstrings and set(words).isdisjoint(filtersetofstrings):
                    continue
                if words[0] == "rt":
                    continue
                else:
                    sents = sent_tokenize(text)
                    for sentence in sents:
                        question = False
                        logger(sentence, debug)
                        words = word_tokenize(sentence)
                        sentencelist = sentencelist + sents
            except KeyError:
                if str(tw) != "{}":  # never mind empty strings, no cause for alarm
                    logger("**** " + str(tw) + " " + str(len(sentencelist)), error)
    return sentencelist


# to make use of nltk without having to import it to surrounding projects
def words_of_a_sentence(sentence: str):
    words = word_tokenize(sentence)
    return words



# show_uri	show_name show_description	publisher	language	rss_link	episode_uri	episode_name	episode_description	duration	show_filename_prefix	episode_filename_prefix
def readtsvfile(filename, loglevel=False):
    '''Read one file with tsv lines such and return the text found in the specified slots.'''
    logger(filename, loglevel)
    sentencelist = []
    with open(filename, errors="replace", newline="", encoding='utf-8') as inputtextfile:
        logger("Loading " + filename, loglevel)
        linereader = csv.reader(inputtextfile, delimiter='\t', quotechar='"')
        for line in linereader:
            id = line[0]
            showdescription = word_tokenize(line[2])
            episodedescription = word_tokenize(line[8])
            episodetitle = word_tokenize(line[7])
            showtitle = word_tokenize(line[1])
    return [id, showtitle, episodetitle, showdescription, episodedescription]
