import PyPDF2
import re, os
import json
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def ConvertPdfToText(file):
    #pdfFileObj = open('./static/test.pdf', 'rb')
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    data = {}

    keys = ["skills", "experience", "education", "awards"]


    for i in keys:
        data[i] = []

    data["id"]=random.randint(1,101)

    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText().encode('utf-8')

    cleanString = re.sub(r"[^a-zA-Z0-9]+", ' ', text )
    stopWordSet = set(stopwords.words('english'))
    tokens = word_tokenize(cleanString)

    #keywords = [word for word in tokens if not word in stop_words]

    for key in keys:
        for word in tokens:
            if word not in stopWordSet:
                data[key].append(word)

    #jsonData = json.dumps(data)

    #file = open('./static/fileText.txt','w')
    #file.write(cleanString)
    #file.close()

    #file = open('./static/fileText.json','w')
    #file.write(jsonData)
    #file.close()
    return data

#output = ConvertPdfToText('./static/test.pdf')
#jsonData = json.dumps(output)
#file = open('./static/fileText.json','w')
#file.write(jsonData)
#file.close()
