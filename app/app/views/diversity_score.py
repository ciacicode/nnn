# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g, jsonify
from watson_developer_cloud import PersonalityInsightsV3
import os
import pdb
from .pdftotext import ConvertPdfToText
import json
import pandas as pd
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


def get_candidates_scores(plain_text):

    #get all personality data from watson
    insights = get_personality_insights(plain_text)

    #parse peronality data from insights
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

    #calculate disc score from ocean score
    dominance_score = -0.023*extraversion_score + 0.126*openness_score - 0.278*agreeableness_score + 0.039*ocean_conscient_score - 0.297*emotional_score
    influence_score = 0.383*extraversion_score + 0.251*openness_score + 0.114*agreeableness_score -0.196*ocean_conscient_score + 0.032*emotional_score
    steadiness_score = -0.063*extraversion_score - 0.234*openness_score + 0.308*agreeableness_score - 0.054*ocean_conscient_score - 0.275*emotional_score
    disc_conscient_score = -0.3*extraversion_score + -0.175*openness_score - 0.157*agreeableness_score + 0.185*ocean_conscient_score + -0.008*emotional_score

    disc_score = {"candidate": {"personality" : {"Dominance" : dominance_score,
                                     "Influence" : influence_score,
                                     "Steadiness" : steadiness_score,
                                     "Conscientiousness" : disc_conscient_score
                                     }
                                }
                    }

    return disc_score

def get_team_scores():
    with open(os.path.join('v1/static/', 'team_scores.csv'), 'r') as csvFile:
        team_score_df = pd.read_csv(csvFile)
        dominance_score = team_score_df['D'].mean()
        influence_score = team_score_df['i'].mean()
        steadiness_score = team_score_df['S'].mean()
        disc_conscient_score = team_score_df['C'].mean()
    disc_score = {"team": {"personality" : {"Dominance" : dominance_score,
                                     "Influence" : influence_score,
                                     "Steadiness" : steadiness_score,
                                     "Conscientiousness" : disc_conscient_score
                                     }
                                }
                    }
    return disc_score

def get_both_scores(data):
    score_list = []
    candidate_score = get_candidates_scores(data)
    team_score = get_team_scores()
    score_list.append(candidate_score)
    score_list.append(team_score)
    print(score_list)
    return score_list

# class DiversityScore(Resource):
#
#     def post(self):
#         if 'file' not in request.files:
#             print ('No file part')
#             #if not, redirect maybe to GET??? to do
#             return redirect(request.url)
#         else:
#             file = request.files['file']
#             #save file to folder
#             file.save(os.path.join('v1/static/', file.filename))
#             #data is the text output from the convert function
#             data = ConvertPdfToText(os.path.join('v1/static/', file.filename))
#
#             result = get_both_scores(data)
#
#             return jsonify(result)
