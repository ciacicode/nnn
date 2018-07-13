import PyPDF2
import nltk
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import unicodedata
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

folder = './sample_input/'
filenames = []

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        filenames.append(os.path.join(folder, file))

stopword_set = set(stopwords.words('english'))
output_dict = {}
lmtzr = WordNetLemmatizer()

for filename in filenames:
    pdfFileObj = open(filename, 'rb')
    reader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = reader.numPages
    count = 0
    text = ""

    while count<num_pages:
        pageObj = reader.getPage(count)
        count = count+1
        text = text + pageObj.extractText().encode('utf-8')

    if text!='':
        text=text

    tokenizer = RegexpTokenizer(r'\w+')
    wordlist = tokenizer.tokenize(text.decode('utf-8'))

    for w in wordlist:
        w = lmtzr.lemmatize(w.lower())
        if w not in stopword_set:
            if wordnet.synsets(w):
                if w not in output_dict.keys():
                    output_dict[w] = 1
                else:
                    output_dict[w] = output_dict[w]+1

for key, value in sorted(output_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    print "%s: %s" % (key, value)
