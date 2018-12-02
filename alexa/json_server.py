from flask import Flask, Response, request
import json
import gkeep

app = Flask(__name__)
application = app

"""
Doc at:
https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#response-format

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
        list_name = intent['slots']['list_name']['value']
        list_id = gkeep.LISTS[list_name]
        gkeep.read_list(keep, list_id)

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
        list_name = intent['slots']['list_name']['value']
        list_id = gkeep.LISTS[list_name]
        keep = alexa.login()
        gkeep.add_to_list(keep, list_id)
        dict_response = {'version': "1.0",
                        "response": {"outputSpeech": {'type': 'PlainText', 'text': f'adding {item} to {list_name} list'}}}
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
