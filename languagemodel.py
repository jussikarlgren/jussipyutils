from logger import logger
from math import log
from math import exp
from math import atan, pi
error = True  # log level


class LanguageModel:
    """Tracks occurrence frequencies of observed items and provides frequency-based weights for the same."""
    def __init__(self):
        self.globalfrequency = {}
        self.bign = 0
        self.df = {}
        self.docs = 1
        self.changed = False
        self.filename = None
        self.maxdf = 1
        self.maxfreq = 0

    def observedfrequency(self, item):
        if item in self.globalfrequency:
            return self.globalfrequency[item]
        else:
            return 0

    def frequencyweight2(self, word, streaming=True):
        '''Needs work'''
        try:
            if streaming:
                ell = 500
                w = exp(-ell * self.globalfrequency[word] / self.bign)
                #
                #
            else:
                if word in self.df:
                    w = atan(0.5 + self.docs / self.df[word]) / (0.5 * pi)  # ranges between 1 and 1/3
                else:
                    w = atan(0.5 + self.bign / self.globalfrequency[word]) / (0.5 * pi)  # ranges between 1 and 1/3
        except (ValueError, KeyError):
            w = 0.3
        return w

    def hiloweight(self, word):
        '''Experimental'''
        noise = 10
        try:
            if word in self.df:
                interest = self.maxdf / 5
                stop = self.maxdf / 3
                wf = self.df[word]
            else:
                interest = self.maxfreq / 4
                stop = self.maxfreq / 2
                wf = self.globalfrequency[word]
            if wf < noise:  # oov or typo or summat
                w = 0.3
            elif wf < interest:  # interesting word
                w = 0.9
            elif wf < stop:  # frequent word
                w = 0.2
            else:
                w = 0.1   # stopword
        except (ValueError, KeyError):
            w = 0.3
        return w

    def frequencyweight(self, word, streaming=True):
        return self.hiloweight(word)

    def additem(self, item, frequency=0):
        if not self.contains(item):
            self.globalfrequency[item] = frequency
            if frequency > self.maxfreq:
                self.maxfreq = frequency
            self.df[item] = 1
            self.bign += frequency
            self.changed = True

    def removeitem(self, item):
        self.bign -= self.globalfrequency[item]
        del self.globalfrequency[item]
        self.changed = True

    def observe(self, word):
        self.bign += 1
        if self.contains(word):
            self.globalfrequency[word] += 1
        else:
            self.globalfrequency[word] = 1
        self.changed = True

    def contains(self, item):
        if item in self.globalfrequency:
            return True
        else:
            return False

    def importstats(self, wordstatsfile: str) -> None:
        """ Read file with lines of item-tab-item frequency to provide basis for weighting etc. """
        self.filename = wordstatsfile
        try:
            with open(wordstatsfile) as savedstats:
                i = 0
                for line in savedstats:
                    i += 1
                    try:
                        seqstats = line.rstrip().split("\t")
                        if not self.contains(seqstats[0]):
                            self.additem(seqstats[0])
                        self.globalfrequency[seqstats[0]] = int(seqstats[1])
                        if self.maxfreq < self.globalfrequency[seqstats[0]]:
                            self.maxfreq = self.globalfrequency[seqstats[0]]
                        if len(seqstats) > 2:
                            self.df[seqstats[0]] = int(seqstats[2])
                            if self.maxdf < self.df[seqstats[0]]:
                                self.maxdf = self.df[seqstats[0]]
                            self.docs += int(seqstats[2])
                        self.bign += int(seqstats[1])
                    except IndexError:
                        logger(str(i) + " " + line.rstrip(), error)
        except FileNotFoundError:
            logger("Could not open {}".format(wordstatsfile), error)

    def save(self) -> None:
        if self.filename:
            with open(self.filename, "w+") as savedstats:
                for w in self.globalfrequency:
                    savedstats.write("{}\t{}\n".format(w, self.globalfrequency[w]))
        else:
            logger("No outfilename defined", error)
        self.changed = False
