# libs
from RecommendationSys import final_recommendations
from io import StringIO    
import json
import flask
from flask import Flask, request
import time
from flask import jsonify

def __init__(self,UserId,ArticleId):
    self.UserId = UserId
    self.ArticleId = ArticleId


def get_recommendations(json):
    recommendations = final_recommendations(json['UserId'],json['ArticleId'])
    return recommendations



app = Flask(__name__)

@app.route('/ping',methods=['GET'])
@app.route('/',methods=['POST'])


def recommend():
    if flask.request.content_type == 'application/json':
        input_json = flask.request.get_json()
        print("Input json")
        print(input_json)
    else:
        return flask.Response(response='Content type should be application/json', status=415, mimetype='application/json')
    response = get_recommendations_en_gb(input_json)

# Get the response
    out = StringIO()    
    json.dump(response, out)
    return flask.Response(response=out.getvalue(), status=200, mimetype='application/json')

    
if __name__ == '__main__':
       
    app.run(port=8000)
