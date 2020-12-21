import simpletextfilereader
from nltk import sent_tokenize
from random import random
import json
from splitstream import splitfile


# class BrownCorpus(object):
class MicroblogCorpus(object):
    samplingrate = 0.1

    def __init__(self, s: float = 0.1):
        self.samplingrate = s

    def __iter__(self):
        files = simpletextfilereader.getfilelist("/Users/jik/data/microblog/storm", ".*.EN.twitter.*")
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
        files = simpletextfilereader.getfilelist("/Users/jik/data/socialmedia", ".*blog")
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
        files = simpletextfilereader.getfilelist("/Users/jik/data/blogs", ".*xml")
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
        for line in open("/Users/jik/data/news/apauthor.txt"):
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
        files = simpletextfilereader.getfilelist("/Users/jik/data/podcasts/trec-podcasts/transcript_raw", ".*txt")
        for file in files:
            for line in open(file, "r"):
                sents = sent_tokenize(line)
                for s in sents:
                    if random() < self.samplingrate:
                        yield s
