# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from .pdftotext import ConvertPdfToText
from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from .resume_form import Resume
import pdb
import json

bp = Blueprint('views', __name__, template_folder='templates')
MYDIR = os.path.dirname(__file__)

@bp.route('/')
def show():
    try:
        return render_template("layout.html")
    except TemplateNotFound:
        abort(404)

@bp.route('/resume', methods=['GET', 'POST'])
def unbias():
    form = Resume(request.form)
    if form.validate_on_submit():
        # get resume as file from the form
        file = request.files['resume']
        #file is stored in a folder
        file.save(os.path.join(MYDIR+'/static/', file.filename))
        unbiased = ConvertPdfToText(MYDIR+'/static/'+file.filename)
        return render_template('resume_result.html', result=unbiased)
    else:
        #it's a get request
        return render_template('resume_upload.html', form=form)

@bp.route('/diversity', methods=['GET', 'POST'])
def diversity():
    form = Resume(request.form)
    if form.validate_on_submit():
        # show resume_result
        # call diversity_score functions from shraddha's code
        # store in insights
        insights = [{"candidate":{"personality": {"Dominance": 0.8, "Influence":0.4, "Conscientiousness":0.7,"Steadiness":0.9 }}},
        {"team": {"personality": {"Dominance":0.4, "Influence":0.7, "Conscientiousness":0.4, "Steadiness":0.7 }}}]
        return render_template('diversity_result.html', insights=json.dumps(insights))
    else:
        #it's a get request
        return render_template('diversity_upload.html', form=form)
