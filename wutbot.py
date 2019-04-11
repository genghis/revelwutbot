import gspread
from flask import Flask, request, jsonify 
import requests
from oauth2client.service_account import ServiceAccountCredentials
import os
import json # Yes I KNOW I'm already importing jsonify from flask but this has to do DIFFERENT things. Sigh.

app = Flask(__name__)

@app.route('/', methods=['POST']) # Decorator that does fun web stuff

def lambda_handler(): # 
    text = request.form.get('text') # Text of what the user asked about
    spreadsheeturl = os.environ['spreadsheet'] 
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # The creds variable yanks a Google OAuth2 credentials json file and uses it along with the scopes above. These arguments are positional, so if you get fancier, you'll need to be explicit.
    # Also, as a note, I tried incredibly hard to build json from environment variables and couldn't figure out how to make it work with this library.

    creds = ServiceAccountCredentials.from_json_keyfile_name('wutbot.json',scope) # my credentials file is called wutbot.json, yours will be something else
    client = gspread.authorize(creds)

    sheet = client.open('definitions').sheet1 # Pointing to the right spreadsheet.

    # Try/Except here to handle whether the spreadsheet has that value or not. The search is case sensitive for no good reason, so I've got columns in the spreadsheet that just create variously cased versions of every entry automatically. It's a kludge, but it works.

    try:
        location = sheet.find(text)
        answer = sheet.cell(location.row, 2).value
        # Below, I'm creating the JSON for "blocks", which are new fancy features for nicely formatted messages in slack.
        returnvalue = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{text}*:"
                }
            },
                {
                    "type": "divider"
                },
            {
                "type": "section",
                "text": {
                    "type":"mrkdwn",
                    "text": f"> _{answer}_"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Not helpful enough? Once you find the definition, add it at:\n{spreadsheeturl}"
                    }
                ]
            }
            ]

        jsonreturn = json.dumps(returnvalue) # Turn that list into a string
        return jsonify(blocks=jsonreturn) # Make it pretty and append "blocks" so Slack knows how to interpret it.
    except:
        return f"Couldn't find '{text}'. Once you have an answer, please add it to {spreadsheeturl}"
