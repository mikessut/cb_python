from flask import Flask, Response, request
import json

app = Flask(__name__)
application = app

"""
Doc at:
https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#response-format

"""

CHECKLIST = ['kindle',
'tablet',
'mouse',
'computer charger',
'roku',
'router',
'usb chargers',
'jacket',
'badge',
'wallet',
'phone',
'closet',
'fridge',]



@app.route('/', methods=['GET', 'POST'])
def index():


    if (request.json is None) or ('request' not in request.json.keys()):
        return Response(response=json.dumps({}),
                    status=200,
                    mimetype="application/json;charset=UTF-8")

    alexa_request = request.json['request']
    session = request.json['session']
    if 'intent' in alexa_request.keys():
        intent = alexa_request['intent']
    else:
        intent = {}

    # print(alexa_request)
    # print(intent)

    if ('type' in alexa_request.keys()) and (alexa_request['type'] == 'LaunchRequest'):

        txt = CHECKLIST[0]
        dict_response = {'version': "1.0",
                         'sessionAttributes': {'listPos': 1},
                         "response": {"outputSpeech": {"type": "PlainText",
                                                       "text": txt},
                                      "shouldEndSession": False}}
        resp = Response(response=json.dumps(dict_response),
                    status=200,
                    mimetype="application/json;charset=UTF-8")
    elif ('name' in intent.keys()) and (intent['name'] == 'continue'):
        listPos = session['attributes']['listPos']
        if listPos == len(CHECKLIST):
            dict_response = {'version': "1.0",
                             'sessionAttributes': {'listPos': 1},
                          "response": {"outputSpeech": {"type": "PlainText",
                                                        "text": "checklist complete"}}}
            resp = Response(response=json.dumps(dict_response),
                    status=200,
                    mimetype="application/json;charset=UTF-8")
        else:
            dict_response = {'version': "1.0",
                             'sessionAttributes': {'listPos': listPos + 1},
                          "response": {"outputSpeech": {"type": "PlainText",
                                                        "text": CHECKLIST[listPos]},
                                       "shouldEndSession": False}}
            resp = Response(response=json.dumps(dict_response),
                    status=200,
                    mimetype="application/json;charset=UTF-8")

    else:
        print("Unknown intent")
        dict_response = {'version': "1.0",
                        "response": {"outputSpeech": {'type': 'PlainText', 'text': 'unknown or intent not specified'}}}
        resp = Response(response=json.dumps(dict_response),
                    status=200,
                    mimetype="application/json;charset=UTF-8")
    return resp

if __name__ == '__main__':
    #print(json.loads(test_response))
    app.run(debug=True, port=4001)
