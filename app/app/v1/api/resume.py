# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g
from flask_wtf import Form
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
            #you must return an object that matches the schemas description in schemas.py
            return {"id": 0,"skills": [ "string"],"experience": ["string"],"education": ["string"]}, 201, None
