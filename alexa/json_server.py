from flask import Flask, Response, request
import json
import alexa

app = Flask(__name__)
application = app

"""
Doc at:
https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#response-format

"""

test_response = """
{
  "version": "1.0",
  "sessionAttributes": {
    "key": "value"
  },
  "response": {
    "outputSpeech": {
      "type": "PlainText",
      "text": "Plain text string to speak",
      "ssml": "<speak>SSML text string to speak</speak>",
      "playBehavior": "REPLACE_ENQUEUED"
    }
  },
    "shouldEndSession": true
  }
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    #return "Hello, World!"

    # print(request.args)
    # print(request.values)
    # print(request.form)
    # print(request.json)

    alexa_request = request.json['request']
    if 'intent' in alexa_request.keys():
        intent = alexa_request['intent']
    else:
        intent = {}

    # print(alexa_request)
    # print(intent)

    if ('name' in intent.keys()) and (intent['name'] == 'read_list'):
        keep = alexa.login()
        l = alexa.grocery_list(keep)
        # print("list:",l)

        ssmltxt = '<speak>'
        ssmltxt += ''.join(x + '<break strength="medium"/>' for x in l)
        ssmltxt += '</speak>'
        # print(ssmltxt)
        dict_response = {'version': "1.0",
                         "response": {"outputSpeech": {"type": "SSML", "ssml": ssmltxt}}}

        resp = Response(response=json.dumps(dict_response),
                    status=200,
                    mimetype="application/json;charset=UTF-8")
    elif ('name' in intent.keys()) and (intent['name'] == 'add_to_list'):
        item = intent['slots']['item']['value']
        keep = alexa.login()
        alexa.add2grocery(keep, item)
        dict_response = {'version': "1.0",
                        "response": {"outputSpeech": {'type': 'PlainText', 'text': f'adding {item} to grocery list'}}}
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
