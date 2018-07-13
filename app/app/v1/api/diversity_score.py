# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask_wtf import Form
from flask import request, g, jsonify
from wtforms import SubmitField, TextAreaField, validators, ValidationError
from watson_developer_cloud import PersonalityInsightsV3
from datetime import datetime, date
import os
import pdb
from .pdfToText import ConvertPdfToText
import json

from . import Resource
from .. import schemas
from config import Config

def get_personality_insights(profile):
    """
    profile: text input
    returns raw data from watson personality api
    adds calls to database to track service usage
    """
    personality_insights = PersonalityInsightsV3(
        version='2016-10-20',
        username=Config.WATSON['username'],
        password=Config.WATSON['password'])
    #check if we still have enough calls
    today = date.today()
    year = today.year
    month = today.month
    personality = personality_insights.profile(profile, content_type='text/plain;charset=utf-8',raw_scores=True, consumption_preferences=True)
    #serialise to string and then to object
    result = json.loads(json.dumps(personality))
    return result

def generate_data(insights, category='personality'):
    """
    insights: as json from watson
    category: one between needs (default), consumption_preferences, values, personality
    returns data: ready for chart display
    """
    try:
    #category
        data = insights[category]
        #generate dimensions of each category to be used as labels
        raw_scores = list()
        percentiles = list()
        labels = list()

        for dimension in data:
            #create array of data
            labels.append(dimension['name'])
            raw_scores.append(dimension['raw_score'])
            percentiles.append(dimension['percentile'])
        #craft output data Structure
        chart_data = dict([('labels', labels), ('raw_scores', raw_scores), ('percentiles', percentiles)])
        return chart_data
    except KeyError as ke:
        print("ke")
    except TypeError as te:
        print("te")


def generate_all_data(insights):
    """
    insights: as json from watson
    returns an object containing data for each dimension and hence chart
    """
    all_data = dict()
    for dimension in insights.keys():
        if dimension in ['warnings','word_count','processed_language', 'consumption_preferences']:
            #we don't care
            continue
        else:
            #it's a dimension we want
            chart_data = generate_data(insights,dimension)
            all_data[dimension] = chart_data
    return all_data

class DiversityScore(Resource):

    def post(self):
        if 'file' not in request.files:
            print ('No file part')
            #if not, redirect maybe to GET??? to do
            return redirect(request.url)
        else:
            file = request.files['file']
            #save file to folder
            file.save(os.path.join('v1/static/', file.filename))
            #data is the text output from the convert function
            data = ConvertPdfToText(os.path.join('v1/static/', file.filename))
            insights = get_personality_insights(data)
            data = generate_data(insights, category='personality')
            labels = data.get('labels')
            raw_scores = data.get('raw_scores')
            for index, label in enumerate(labels):
                if label == 'Openness':
                    openness_score = raw_scores[index]
                if label == 'Conscientiousness':
                    ocean_conscient_score = raw_scores[index]
                if label == 'Extraversion':
                    extraversion_score = raw_scores[index]
                if label == 'Agreeableness':
                    agreeableness_score = raw_scores[index]
                if label == 'Emotional range':
                    emotional_score = raw_scores[index]
            #print(openness_score, conscient_score, extraversion_score, agreeableness_score, emotional_score)
            dominance_score = -0.023*extraversion_score + 0.126*openness_score - 0.278*agreeableness_score + 0.039*ocean_conscient_score - 0.297*emotional_score
            influence_score = 0.383*extraversion_score + 0.251*openness_score + 0.114*agreeableness_score -0.196*ocean_conscient_score + 0.032*emotional_score
            steadiness_score = -0.063*extraversion_score - 0.234*openness_score + 0.308*agreeableness_score - 0.054*ocean_conscient_score - 0.275*emotional_score
            disc_conscient_score = -0.3*extraversion_score + -0.175*openness_score - 0.157*agreeableness_score + 0.185*ocean_conscient_score + -0.008*emotional_score
            disc_score = {"personality" : {"dominance" : dominance_score,
                                     "influence" : influence_score,
                                     "steadiness" : steadiness_score,
                                     "conscientiousness" : disc_conscient_score}}
            return disc_score, 201, None
