# Nearly Nameless Nick
## A MiQ hackathon project
Nearly Nameless Nick is an API aimed at removing unconscious bias that may exist in your organisation when hiring new employees. It helps at different stages of the hiring process:
1. CV screening
2. Interviewer selection
3. Hiring decision

---

## Getting Started
1. Clone this repository
2. Set up your virtual environment with [conda](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/)
3. Install from ```pip install -r requirements.txt```
4. Activate your virtual environment from the terminal  
5. Navigate to root of project ```$ cd app/app```
6. Execute with environment ```python __init__.py```
7. Check root endpoint for full Swagger documentation

## How to contribute
Clone this repository and apply your changes, then open a pull request for approval.

* ```core``` stores the business logic
* ```apis``` stores the different namespaces a.k.a objects handled by the API
* ```app``` handles the endpoints of the API

This prototype is built with [Flask Restplus](http://flask-restplus.readthedocs.io/en/latest/index.html)
