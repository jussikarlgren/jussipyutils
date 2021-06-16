import simpletextfilereader
from nltk import sent_tokenize
from random import random, shuffle
import json
#from splitstream import splitfile


datadirectory = "/Users/jik/data/"


class SwitchboardCorpus(object):
    samplingrate = 0.1

    def __init__(self, s: float = 0.7):  # corpus is small
        self.samplingrate = s

    def __iter__(self):
        files = simpletextfilereader.getfilelist(datadirectory + "switchboard/cleaned", ".*utt")
        shuffle(files)
        for file in files:
            for utterance in open(file, "r"):
                if random() < self.samplingrate:
                    yield utterance


class MovieDialogueCorpus(object):
    samplingrate = 0.3

    def __init__(self, s: float = 0.3):
        self.samplingrate = s

    def __iter__(self):
        files = simpletextfilereader.getfilelist(datadirectory + "moviescriptsUCSC/cleaned_jan_2021", ".*txt")
        shuffle(files)
        for file in files:
            for line in open(file, "r"):
                sents = sent_tokenize(line)
                for s in sents:
                    if random() < self.samplingrate:
                        yield s


class MicroblogCorpus(object):
    samplingrate = 0.1

    def __init__(self, s: float = 0.1):
        self.samplingrate = s

    def __iter__(self):
        files = simpletextfilereader.getfilelist(datadirectory + "microblog/storm", ".*.EN.twitter.*")
        shuffle(files)
        for file in files:
            with open(file, "r+") as fff:
                for jsonstr in splitfile(fff, format="json"):
                    data = json.loads(jsonstr)
                    sents = sent_tokenize(data["rawText"])
                    for s in sents:
                        if random() < self.samplingrate:
                            yield s


class NotReallyBlogCorpusBecause2017ItWasAllNewsAndSpam(object):
    samplingrate = 0.1

    def __init__(self, s: float = 0.1):
        self.samplingrate = s

    def __iter__(self):
        files = simpletextfilereader.getfilelist(datadirectory + "socialmedia", ".*blog")
        shuffle(files)
        for file in files:
            with open(file, "r+") as fff:
                for jsonstr in splitfile(fff, format="json"):
                    data = json.loads(jsonstr)
                    sents = sent_tokenize(data["rawText"])
                    for s in sents:
                        if random() < self.samplingrate:
                            yield s


class BlogCorpus(object):
    samplingrate = 0.1

    def __init__(self, s: float = 0.1):
        self.samplingrate = s

    def __iter__(self):
        files = simpletextfilereader.getfilelist(datadirectory + "blogs", ".*xml")
        shuffle(files)
        j = 0
        for file in files:
            i = 0
            prev = None
            for line in open(file, "r+", errors='ignore'):
                i += 1
                j += 1
                prev = line
                if line.startswith("<"):
                    continue
                if len(line) < 10:
                    continue
                sents = sent_tokenize(line)
            for s in sents:
                if random() < self.samplingrate:
                    yield s


class NewsCorpus(object):
    samplingrate = 0.1

    def __init__(self, s: float = 0.1):
        self.samplingrate = s

    def __iter__(self):
        for line in open(datadirectory + "news/apauthor.txt"):
            # assume there's one document per line, tokens separated by whitespace
            (author, article) = line.split("\t")
            sents = sent_tokenize(article)
            for s in sents:
                if random() < self.samplingrate:
                    yield s.lstrip().rstrip()


class PodcastTranscriptCorpus(object):
    samplingrate = 0.1

    def __init__(self, s: float = 0.1):
        self.samplingrate = s

    def __iter__(self):
        files = simpletextfilereader.getfilelist(datadirectory + "podcasts/transcript_raw", ".*txt")
        shuffle(files)
        for file in files:
            for line in open(file, "r"):
                sents = sent_tokenize(line)
                for s in sents:
                    if random() < self.samplingrate:
                        yield s
