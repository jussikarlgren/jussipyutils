import corenlp

tag = "3"


class InterestingSentencesCorpus(object):
    def __iter__(self, samplingrate: float = 0.1):
        types = ["nw", "bl", "tw", "pd"]
        for one in types:
            file = "/Users/jik/data/nov." + one + ".list"
            with open(file, "r+") as fff:
                for s in fff:
                    yield s


with corenlp.CoreNLPClient(annotators="tokenize ssplit pos lemma ner depparse".split()) as client:
    for text in InterestingSentencesCorpus():
        ann = client.annotate(text)
        with open("/Users/jik/tmp/corenlpoutput."+tag+".txt", "a+") as outfile:
            outfile.write(str(ann))
            outfile.write("\n")
