import PyPDF2
import re
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pdb

def ConvertPdfToText(file):
    #pdfFileObj = open('./static/test.pdf', 'rb')
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    data = {}

    keys = ["skills", "experience", "education"]


    for i in keys:
        data[i] = []

    data["id"]=123

    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText().encode('utf-8')
    if text != "":
       text = text

    cleanString = re.sub(r"[^a-zA-Z0-9]+", ' ', text )
    stopWordSet = set(stopwords.words('english'))
    tokens = word_tokenize(cleanString)

    #keywords = [word for word in tokens if not word in stop_words]

    c=0
    for key in keys:
        for word in tokens:
            if word not in stopWordSet:
                data[key].append(word)
                c=c+1
                if c==10:
                    break


    #jsonData = json.dumps(data)

    #file = open('./static/fileText.txt','w')
    #file.write(cleanString)
    #file.close()

    #file = open('./static/fileText.json','w')
    #file.write(jsonData)
    #file.close()
    return json.dumps(data)

#output = ConvertPdfToText('./static/test.pdf')
#jsonData = json.dumps(output)
#file = open('./static/fileText.json','w')
#file.write(jsonData)
#file.close()
