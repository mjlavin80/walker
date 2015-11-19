import nltk
from nltk.stem import WordNetLemmatizer
from collections import Counter
from BeautifulSoup import BeautifulSoup
import string
import urllib
import re
import enchant

class ProcessedText():
    def __init__(self, original_text, purge_html=None, title='untitled', authorship='unknown'):
        if purge_html is None:
            purge_html = True
        self.title = title
        self.authorship = authorship
        self.purge_html = purge_html
        self.original_text = original_text
        self.dist = {}
        self.process() #define last
        # convert fields to utf-8 if text

    def process(self):
        self.decode_encode_utf8()
        self.tokenize()
        self.special_for_simple()
        self.hyphen_split()
        self.punct_strip()
        self.freq_dist()

    def decode_encode_utf8(self):
        try:
            self.original_text = self.original_text.decode('utf-8')
        except UnicodeDecodeError:
            pass
        try:
            if isinstance(self.original_text, basestring):
                #wrap all encodes in a try?
                try:
                    mystring = self.original_text.encode('utf-8', 'replace')
                except:
                    #mystring = BeautifulSoup(self.original_text).getText().encode('utf-8')
                    mystring = unicode(BeautifulSoup(self.original_text)).encode('utf-8')
            else:
                #wrap all encodes in a try?
                try:
                    mystring = str(self.original_text).encode('utf-8', 'replace')
                except:
                    #mystring = BeautifulSoup(self.original_text).getText().encode('utf-8')
                    mystring = unicode(BeautifulSoup(self.original_text)).encode('utf-8')
        except:
            if isinstance(self.original_text, basestring):
                #wrap all encodes in a try?
                try:
                    mystring = self.original_text.decode('utf-8').encode('utf-8', 'replace')
                except:
                    #mystring = BeautifulSoup(self.original_text).getText().encode('utf-8')
                    mystring = unicode(BeautifulSoup(self.original_text)).encode('utf-8')
            else:
                #wrap all encodes in a try?
                try:
                    mystring = str(self.original_text.decode('utf-8')).encode('utf-8', 'replace')
                except:
                    #mystring = BeautifulSoup(self.original_text).getText().encode('utf-8')
                    mystring = unicode(BeautifulSoup(self.original_text)).encode('utf-8')
        mystring = mystring.replace("\n", " ").replace("\t", " ")
        self.utf8 = mystring
    def tokenize(self):
        self.tokens = self.utf8.lower().split(' ')

    def special_for_simple(self):
        self.tokens_fixed = []
        for m in self.tokens:
            t = """\xe2\x80\x93"""
            t2 = """\xe2\x80\x94"""
            regex = re.compile(t)
            fixed_token = regex.sub("-", m)

            regex = re.compile(t2)
            fixed_token = regex.sub("-", fixed_token)
            self.tokens_fixed.append(fixed_token)

    def hyphen_split(self):
        d = enchant.Dict("en_US")
        self.tokens_hyphen_split = []
        for i in self.tokens_fixed:
            if '-' in i:
                term_list = i.split('-')
                e = False
                try:
                    e = all(d.check(j) == True for j in term_list)
                except:
                    pass
                if e == True:
                    self.tokens_hyphen_split.extend(term_list)
                else:
                    self.tokens_hyphen_split.append(''.join(term_list))
            else:
                    self.tokens_hyphen_split.append(i)
    def punct_strip(self):
        self.tokens_no_punct = []
        for i in self.tokens_hyphen_split:
            if i.isalpha() == True:
                self.tokens_no_punct.append(i)
            else:
                word= ""
                for j in i:
                    if j.isalpha() == True:
                        word+=j
                self.tokens_no_punct.append(word)
                self.tokens_no_punct = [i for i in self.tokens_no_punct if i != '']
    def freq_dist(self):
        self.dist = Counter(self.tokens_no_punct)

    def lemmatize(self):
        wnl = WordNetLemmatizer()
        self.lemma_list = []

        for i in self.tokens_no_punct:
            lemmy_word = wnl.lemmatize(i)
            self.lemma_list.append(unicode(lemmy_word))

    def lemma_dist(self):
        self.lemma_counts = Counter(self.lemma_list)

    def pos_tag(self):
        #parts of speech
        self.pos_tuples = nltk.pos_tag(self.tokens_no_punct)

if __name__ == '__main__':
    #In the interpreter, type and press enter after each line...
    """
    a = "hello" + chr(255)

    a

    print a

    unicode(a)

    unicode(a, errors='ignore')
    type(unicode(a, errors='ignore'))

    a.decode('latin1')
    type(a.decode('latin1'))

    print a.decode('latin1')
    """

    with open('walker_corrected_a.txt') as f:
        a = f.read()
        b = ProcessedText(a)

        print b.tokens_no_punct
    """

    with open('ulthar.txt') as g:
        c = g.read()
        d = ProcessedText(c)

        print d.tokens_no_punct
        """
