# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask_wtf import Form
from flask import request, g
from wtforms import SubmitField, TextAreaField, validators, ValidationError
from watson_developer_cloud import PersonalityInsightsV3
from datetime import datetime, date
import json

from . import Resource
from .. import schemas
from config import Config

class Profile(Form):
    profile = TextAreaField('profile', [validators.Required()])
    submit = SubmitField('Calculate')

    def validate_profile(form, field):
        """
        Checks there are min 120 words
        """
        profile = field.data
        words = profile.split(" ")
        if len(words) < 120:
            raise ValidationError('Profile must have more than 120 words. Try harder!')

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

def generate_data(insights, category='needs'):
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
        #print(g.form)

        mock_score = {"personality": {"dominance": 0, "steadiness": 0,"conscientiousness": 0,"influence": 0}}
        return mock_score, 200, None
