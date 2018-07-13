# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.resume import Resume
from .api.diversity_score import DiversityScore


routes = [
    dict(resource=Resume, urls=['/resume'], endpoint='resume'),
    dict(resource=DiversityScore, urls=['/diversity_score'], endpoint='diversity_score'),
]