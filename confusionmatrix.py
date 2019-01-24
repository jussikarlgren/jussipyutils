from random import random
class ConfusionMatrix:
    '''ConfusionMatrix keeps book over a categorisation excercise, most notably its errors.

    Use as follows:
        a = ConfusionMatrix()
        for each item:
            a.addconfusion(correct_label, predicted_label)


        a.evaluate()
    '''
    def __init__(self):
        self.confusionmatrix = {}
        self.gold = set()         # actual labels
        self.glitter = set()      # predicted labels
        self.weight = {}          # number of actual items for a category
        self.glitterweight = {}   # number of items with a category label
        self.carat = {}           # number of items with the correct label
        self.macro = 0
        self.micro = 0

    def addconfusion(self, rfacit, rpredicted):
        facit = str(rfacit)
        self.gold.add(facit)
        predicted = str(rpredicted)
        self.glitter.add(predicted)
        if facit in self.confusionmatrix:
            if predicted in self.confusionmatrix[facit]:
                self.confusionmatrix[facit][predicted] += 1
            else:
                self.confusionmatrix[facit][predicted] = 1
        else:
            self.confusionmatrix[facit] = {}
            self.confusionmatrix[facit][predicted] = 1

    def evaluate(self, full=True):
        margin = 4
        decimals = 4
        # HEADER LINE
        labellength = len("correct")  # longest fixed header string
        for glitterlabel in sorted(self.glitter):
            if len(glitterlabel) > labellength:
                labellength = len(glitterlabel)
        fieldlength = margin + labellength
        print(" " * fieldlength + "|", end="")
        for glitterlabel in sorted(self.glitter):
            print((" " * (margin - 1) + "{:" + str(labellength) + "s} ").format(glitterlabel), end="|")
            self.glitterweight[glitterlabel] = 0
        print(((" " * margin + "{:" + str(labellength) + "s}") * 3).format("sum", "correct", "recall"))
        # SEPARATOR LINE
        for gg in range(4 + len(self.glitter)):
            print("-" * fieldlength, end="+")
        print()

        hsum = 0
        correct = 0
        for goldlabel in sorted(self.gold):
            print((" " * (margin - 1) + "{:" + str(labellength) + "s} ").format(goldlabel), end="|")
            self.weight[goldlabel] = 0
            self.carat[goldlabel] = 0
            for glitterlabel in sorted(self.glitter):
                try:
                    print((" " * (margin - 1) + "{:" + str(labellength) + "}").format(self.confusionmatrix[goldlabel][glitterlabel]), end=" ")
                    self.weight[goldlabel] += self.confusionmatrix[goldlabel][glitterlabel]
                    self.glitterweight[glitterlabel] += self.confusionmatrix[goldlabel][glitterlabel]
                    if glitterlabel == goldlabel:
                        self.carat[goldlabel] = self.confusionmatrix[goldlabel][glitterlabel]
                except KeyError:
                    print((" " * (margin - 1) + "{:{}}").format(0, labellength), end=" ")
            print((" |" + (" " * margin + "{:" + str(labellength) + "}") * 2 + " " * margin + "{:." + str(decimals) + "}").format(self.weight[goldlabel],
                                                                                      self.carat[goldlabel],
                                                                                      self.carat[goldlabel] / self.weight[goldlabel]))

            hsum += self.weight[goldlabel]
            correct += self.carat[goldlabel]
            if self.weight[goldlabel] > 0:
                self.macro += self.carat[goldlabel] / self.weight[goldlabel]
        # SEPARATOR LINE
        for gg in range(4 + len(self.glitter)):
            print("-" * fieldlength, end="+")
        print()

        # SUM of PREDICTIONS LINE
        print((" " * (margin - 1) + "{:" + str(labellength) + "s}").format(
            "sum"), end=" |")
        vsum = 0
        for glitterlabel in sorted(self.glitter):
            vsum += self.glitterweight[glitterlabel]
            print((" " * (margin - 1) + "{:{}}").format(self.glitterweight[glitterlabel], labellength), end=" ")
        if hsum > 0:
            self.macro = self.macro / len(self.gold)
            self.micro = correct / hsum
        print((" |" + (" " * margin + "{:" + str(labellength) + "}") * 2).format(
            hsum,
            vsum))
        # CORRECT LINE
        print((" " * (margin - 1) + "{:{}s}").format("correct", labellength), end=" |")
        for glitterlabel in sorted(self.glitter):
            try:
                val = self.carat[glitterlabel]
            except KeyError:
                val = 0
            print((" " * (margin - 1) + "{:{}}").format(val, labellength), end=" ")
        print(" |")
        # PRECISION LINE
        print((" " * (margin - 1) + "{:{}s}").format("prec", labellength), end=" |")
        for glitterlabel in sorted(self.glitter):
            try:
                val = self.carat[glitterlabel] / self.glitterweight[glitterlabel]
            except:
                val = 0.0
            print((" " * margin + "{:.{}f}" + " " * (fieldlength - decimals - margin - 2)).format(val, decimals), end="")
#            print((" " * margin + "{:.{}f} ").format(val, decimals), end="")
        print(" |")
        print((" " * (margin - 1) + "{:{}s}").format("macro", labellength), end=" |")
        print((" " * margin + "{:.{}}" + " " * (fieldlength - decimals)).format(self.macro, decimals))
        print((" " * (margin - 1) + "{:{}s}").format("micro", labellength), end=" |")
        print((" " * margin + "{:.{}}" + " " * (fieldlength - decimals)).format(self.micro, decimals))

        return self.macro

if __name__ == "__main__":
    c = ConfusionMatrix()
    for r in range(int(100*random())):
        c.addconfusion("left","left")
    for r in range(int(100*random())):
        c.addconfusion("right","left")
    for r in range(int(100*random())):
        c.addconfusion("left","right")
    for r in range(int(100*random())):
        c.addconfusion("right","right")
    c.evaluate()
    c = ConfusionMatrix()
    for r in range(int(100*random())):
        c.addconfusion(1,0)
    for r in range(int(100*random())):
        c.addconfusion(0,1)
    for r in range(int(100*random())):
        c.addconfusion(1,1)
    for r in range(int(100*random())):
        c.addconfusion(0,0)
    c.evaluate()
    c = ConfusionMatrix()
    for r in range(int(100*random())):
        c.addconfusion("reallylonglabel",0)
    for r in range(int(100*random())):
        c.addconfusion("reallylonglabel","reallylonglabel")
    c.evaluate()
