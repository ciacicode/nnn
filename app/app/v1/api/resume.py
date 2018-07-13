# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g
from flask_wtf import Form
import os
import json
from .pdfToText import ConvertPdfToText
import pdb

from . import Resource
from .. import schemas

ALLOWED_EXTENSIONS = set(['pdf'])

class Resume(Resource):

    def post(self):
        #check if file argument is in request
        if 'file' not in request.files:
            print ('No file part')
            #if not, redirect maybe to GET??? to do
            return redirect(request.url)
        else:
            file = request.files['file']
            #file is a binary from the post request
            #save file to folder
            file.save(os.path.join('v1/static/', file.filename))
            #data is the text output from the convert function
            unbiased = ConvertPdfToText(os.path.join('v1/static/', file.filename))
            #you must return an object that matches the schemas description in schemas.py
            return json.loads(unbiased), 201, None
