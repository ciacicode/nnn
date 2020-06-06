# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 19:43:34 2018

@author: shraddha
"""

class Config(object):
    WATSON = {
            "url": "https://gateway.watsonplatform.net/personality-insights/api",
            "username": "",
            "password": "",
            "limit" : "300"
}
    SECRET_KEY = "notsosecret"
    UPLOAD_FOLDER ='/v1/static'
