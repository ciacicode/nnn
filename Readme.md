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
5. Type ```python``` to open console and then do
```
import nltk
nltk.download("stopwords")
nltk.download('punkt')

```
6. Navigate to root of project ```$ cd app/app```
7. Execute with environment ```python __init__.py```
8. Check root endpoint for full Swagger documentation

## How to contribute
Clone this repository and apply your changes, then open a pull request for approval.

* ```validators``` store any request validators
* ```api``` stores the classes of objects to be created (POST) and responded (GET) etc
* ```routes``` handles the endpoints of the API
* ```schemas``` handles the response objects
* ```templates``` handles all html pages of this app
