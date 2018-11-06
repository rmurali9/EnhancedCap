from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud.tone_analyzer_v3 import ToneInput

# If service instance provides API key authentication
service = ToneAnalyzerV3(
     ## url is optional, and defaults to the URL below. Use the correct URL for your region.
     url='https://gateway.watsonplatform.net/tone-analyzer/api',
     version='2017-09-21',
     iam_apikey='apikey')

print("\ntone_chat() example 1:\n")
utterances = [{
    'text': 'I am very happy.',
    'user': 'glenn'
}, {
    'text': 'It is a good day.',
    'user': 'glenn'
}]
tone_chat = service.tone_chat(utterances).get_result()
print(json.dumps(tone_chat))

print("\ntone() example 1:\n")
print(
    json.dumps(
        service.tone(
            tone_input='I am very happy. It is a good day.',
            content_type="text/plain").get_result(),
        indent=2))
