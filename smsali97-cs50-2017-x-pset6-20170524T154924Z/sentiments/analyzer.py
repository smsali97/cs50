import nltk


class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.list1 = []
        self.list2 = []
        fpos = open(positives, "r")
        fneg = open(negatives, "r")
        with fpos as lines:
            for line in lines:
                if not(line.startswith(";")):
                    for word in line.split():
                        self.list1.append(word)
        fpos.close()
        with fneg as lines:
            for line in lines:
                if not(line.startswith(";")):
                    for word in line.split():
                        self.list2.append(word)
        fneg.close()
        

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        text.lower
        for item in self.list1:
            if item==text:
                return 1
        for item in self.list2:
            if item==text:
                return -1
        return 0        
