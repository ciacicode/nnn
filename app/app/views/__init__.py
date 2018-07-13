# -*- coding: utf-8 -*-
from __future__ import absolute_import


from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

bp = Blueprint('views', __name__, template_folder='templates')

@bp.route('/')
def show():
    try:
        return render_template("layout.html")
    except TemplateNotFound:
        abort(404)

@bp.route('/resume')
def upload():
    def personality():
    from resume_form import Resume
    form = Resume(request.form)
    return render_template('resume_upload.html', form=form)
