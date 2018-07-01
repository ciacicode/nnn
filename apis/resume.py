from flask_restplus import Namespace, Resource, fields
import json
import pdb

api = Namespace('resume', description='Resume related operations')

resume = api.model('Resume', {
    'id': fields.Integer(readOnly=True, description='The resume unique identifier'),
    'data': fields.String(required=True, description='The resume data')
})



class Resume(object):
    def __init__(self):
        # serialise json string into dictionary
        self.counter = 0

    def create(self, data):
        # take self.data and remove bias
        resume['data'] = data
        resume['id'] = self.counter = self.counter + 1
        bias = resume['data'].pop('personal', None)
        # return new resume object
        return resume

#creating an instance
UNBIASED = Resume()
UNBIASED.create({"skills ": ["Python", "Java"],"education": {"University": {"start_year": 2010,"end_year ": 2013 }},"personal": {"name": "Sarah Connor","age ": 28}})

@api.route('/remove_bias')
@api.param('data', 'The resume data')

class Resume(Resource):
    @api.doc('create_unbiased_resume')
    @api.expect(resume)
    #@api.marshal_with(resume, code= 201)
    #marshalling does not support nested objects!
    #https://github.com/noirbizarre/flask-restplus/issues/293
    def post(self):
        '''Create a new task'''
        #creating a new instance with api payload
        return UNBIASED.create(api.payload), 201
