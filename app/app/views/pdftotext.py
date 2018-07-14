import PyPDF2
import re, os
import json
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import docx2txt
from model_ouput_keywords import var
from collections import defaultdict
from nltk.tokenize import sent_tokenize

def ConvertPdfToText(file):
    #pdfFileObj = open('./static/test.pdf', 'rb')
    text = ""
    data = {}
    output_dict={}
    new_output_dict = defaultdict(list)
    keys = ["skills", "experience", "education", "awards"]

    for i in keys:
        data[i] = []

    data["id"]=random.randint(1,101)
    fileName, fileType = os.path.splitext(file)
    FileObj = open(file, 'rb')
    if fileType == '.pdf':
        pdfReader = PyPDF2.PdfFileReader(FileObj)
        num_pages = pdfReader.numPages
        count = 0

        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count +=1
            text += pageObj.extractText().encode('utf-8')
    elif fileType == '.docx':
        text = docx2txt.process(file).encode('utf-8')
    else:
        text = "Invalid File Type\n"



    new_text_temp = text.lower()
    new_text = new_text_temp.split('\n')

    cleanString = re.sub(r"[^a-zA-Z0-9]+", ' ', text )
    #linesList = sent_tokenize(text)
    #return linesList
    li = []
    for k,v in var.items():
        wordSet = set(v)
        for everyLine in new_text:
            wordsLine = everyLine.split(' ')
            wordsLineSet = set(wordsLine)
            #output_dict["skills"] = new_text
            jaccard_score = float(len(wordsLineSet.intersection(wordSet)))/(len(wordsLineSet.union(wordSet))+1)
            #li.append(jaccard_score)
            if jaccard_score>=0.007:
                new_output_dict[k].append(everyLine)

    stopWordSet = set(stopwords.words('english'))
    tokens = word_tokenize(cleanString)

    #keywords = [word for word in tokens if not word in stop_words]
    #output_dict["skills"] = li
    #ACTUAL METHOD
    #for k,v in var.items():
    #    new_set = set(v).intersection(set(tokens))
    #    output_dict[k] = list(new_set)

    #jsonData = json.dumps(data)

    #file = open('./static/fileText.txt','w')
    #file.write(cleanString)
    #file.close()

    #file = open('./static/fileText.json','w')
    #file.write(jsonData)
    #file.close()

    return new_output_dict

#output = ConvertPdfToText('./static/test.pdf')
#jsonData = json.dumps(output)
#file = open('./static/fileText.json','w')
#file.write(jsonData)
#file.close()
