from flask import Flask, Response, request
import json
import thermostat

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

    if (request.json is None) or ('request' not in request.json.keys()):
        return Response(response=json.dumps({}),
                    status=200,
                    mimetype="application/json;charset=UTF-8")
    alexa_request = request.json['request']
    if 'intent' in alexa_request.keys():
        intent = alexa_request['intent']
    else:
        intent = {}

    # print(alexa_request)
    # print(intent)

    if ('name' in intent.keys()) and (intent['name'] == 'get_temp'):
        temp = thermostat.getTemp()

        txt = f"the indoor temperature is {temp}"
        # print(ssmltxt)
        dict_response = {'version': "1.0",
                         "response": {"outputSpeech": {"type": "PlainText",
                                                       "text": txt}}}

        resp = Response(response=json.dumps(dict_response),
                    status=200,
                    mimetype="application/json;charset=UTF-8")
    elif ('name' in intent.keys()) and (intent['name'] == 'set_temp'):
        temp = int(intent['slots']['temp']['value'])
        thermostat.setTemp(temp)
        dict_response = {'version': "1.0",
                        "response": {"outputSpeech": {'type': 'PlainText',
                                                      'text': f'setting the temperature to {temp}'}}}
        resp = Response(response=json.dumps(dict_response),
                    status=200,
                    mimetype="application/json;charset=UTF-8")
    else:
        #print("Unknown intent")
        dict_response = {'version': "1.0",
                        "response": {"outputSpeech": {'type': 'PlainText', 'text': 'unknown or intent not specified'}}}
        resp = Response(response=json.dumps(dict_response),
                    status=200,
                    mimetype="application/json;charset=UTF-8")
    return resp

if __name__ == '__main__':
    #print(json.loads(test_response))
    app.run(debug=True, port=4001)
