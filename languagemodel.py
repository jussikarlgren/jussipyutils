from logger import logger
from math import log
from math import exp
error = True  # log level

class LanguageModel:
    '''Tracks occurrence frequencies of observed items and provides frequency-based weights for the same.'''
    def __init__(self):
        self.globalfrequency = {}
        self.bign = 0
        self.df = {}
        self.docs = 1
        self.changed = False
        self.filename = None

    def observedfrequency(self, item):
        if item in self.globalfrequency:
            return self.globalfrequency[item]
        else:
            return 0

    def frequencyweight(self, word, streaming=True):
        try:
            if streaming:
                l = 500
                w = exp(-l * self.globalfrequency[word] / self.bign)
                #
                # 1 - math.atan(self.globalfrequency[word] - 1) / (0.5 * math.pi)  # ranges between 1 and 1/3
            else:
                if word in self.df:
                    w = log((self.docs) / (self.df[word] - 0.5))
                else:
                    w = log(self.bign / (self.globalfrequency[word]))
        except (ValueError, KeyError):
            w = 0.3
        return w

    def additem(self, item, frequency=0):
        if not self.contains(item):
            self.globalfrequency[item] = frequency
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
        ''' Read file with lines of item-tab-item frequency to provide basis for weighting etc. '''
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
                        if len(seqstats) > 2:
                            self.df[seqstats[0]] = int(seqstats[2])
                        self.bign += int(seqstats[1])
                    except IndexError:
                        logger(str(i) + " " + line.rstrip(), error)
        except:
            logger("Could not open {}".format(wordstatsfile), error)

    def save(self) -> None:
        if self.filename:
            with open(self.filename, "w+") as savedstats:
                for w in self.globalfrequency:
                    savedstats.write("{}\t{}\n".format(w, self.globalfrequency[w]))
        else:
            logger("No outfilename defined", error)
        self.changed = False


