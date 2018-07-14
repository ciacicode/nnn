import PyPDF2
import re, os
import json
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import docx2txt
from model_ouput_keywords import var

def ConvertPdfToText(file):
    #pdfFileObj = open('./static/test.pdf', 'rb')
    text = ""
    data = {}
    output_dict={}
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

    cleanString = re.sub(r"[^a-zA-Z0-9]+", ' ', text )
    stopWordSet = set(stopwords.words('english'))
    tokens = word_tokenize(cleanString)

    #keywords = [word for word in tokens if not word in stop_words]

    for k,v in var.items():
        new_set = set(v).intersection(set(tokens))
        output_dict[k] = list(new_set)

    #jsonData = json.dumps(data)

    #file = open('./static/fileText.txt','w')
    #file.write(cleanString)
    #file.close()

    #file = open('./static/fileText.json','w')
    #file.write(jsonData)
    #file.close()
    return output_dict

#output = ConvertPdfToText('./static/test.pdf')
#jsonData = json.dumps(output)
#file = open('./static/fileText.json','w')
#file.write(jsonData)
#file.close()
