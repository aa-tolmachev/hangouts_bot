# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# pylint: disable=invalid-name
"""
Simple Hangouts Chat bot that responds to events and
messages from a room.
"""
# [START basic-bot]
from flask import Flask
from flask import request
import requests
from flask import make_response
import os
import json
from pandas import DataFrame
import traceback
import logging
from flask import Flask, render_template, request, json

app = Flask(__name__)

@app.route('/test_dm', methods=['GET'])
def test_dm():
    x = 'helloworld'
    space_url = 'https://chat.googleapis.com/v1/spaces/4OpU8gAAAAE/messages'

    params = {
      "cards": [
        {
          "sections": [
            {
              "widgets": [
                {
                  "textParagraph": {
                    "text": "Hi-diddly-done!<br><font color=\"#0000ff\"><b>New issues to Vera:</b></font><br><i>VERA-102</i>"
                  }
                }
              ]
            }
          ]
        }
      ]
    }

    r = requests.post(space_url,
                      json=params)
    
    print(r.status_code)
    print(r.text)
    
    return x

@app.route('/helloworld', methods=['GET'])
def helloworld():
    x = 'helloworld'
    return x

@app.route('/', methods=['POST'])
def home_post():
    """Respond to POST requests to this endpoint.
    All requests sent to this endpoint from Hangouts Chat are POST
    requests.
    """

    data = request.get_json()

    print(data)
    
    resp = None

    if data['type'] == 'REMOVED_FROM_SPACE':
        logging.info('Bot removed from a space')

    else:
        resp_dict = format_response(data)
        resp = json.jsonify(resp_dict)

    return resp

def format_response(event):
    """Determine what response to provide based upon event data.
    Args:
      event: A dictionary with the event data.
    """

    text = ""

    # Case 1: The bot was added to a room
    if event['type'] == 'ADDED_TO_SPACE' and event['space']['type'] == 'ROOM':
        text = 'Thanks for adding me to "%s"!' % event['space']['displayName']

    # Case 2: The bot was added to a DM
    elif event['type'] == 'ADDED_TO_SPACE' and event['space']['type'] == 'DM':
        text = 'Thanks for adding me to a DM, %s!' % event['user']['displayName']

    elif event['type'] == 'MESSAGE':
        text = 'Your message: "%s" , my master <users/100441901391532176964>' % event['message']['text']

    return {'text': text}


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
