# -*- coding: utf-8 -*-
from __future__ import absolute_import


from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from .resume_form import Resume

bp = Blueprint('views', __name__, template_folder='templates')

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
        # show resume_result
        result = {"id": 0,"skills": [ "Python", "Css"],"experience": ["Google", "Import.io"],"education": ["University of Federico II, Naples"]}
        return render_template('resume_result.html', result=result)
    else:
        #it's a get request
        return render_template('resume_upload.html', form=form)

@bp.route('/diversity', methods=['GET', 'POST'])
def diversity():
    form = Resume(request.form)
    if form.validate_on_submit():
        # show resume_result
        result = {'score': 0.5, 'personality': {"Dominance": 0.8, "Influence":0.4, "Conscientiousness":0.7, "Steadiness": 0.9 }}
        return render_template('diversity_result.html', result=result)
    else:
        #it's a get request
        return render_template('diversity_upload.html', form=form)
