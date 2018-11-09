from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud.tone_analyzer_v3 import ToneInput
from argparse import ArgumentParser
import os.path

# If service instance provides API key authentication
service = ToneAnalyzerV3(
     ## url is optional, and defaults to the URL below. Use the correct URL for your region.
     url='https://gateway.watsonplatform.net/tone-analyzer/api',
     version='2017-09-21',
     iam_apikey= 'hTpIqPFChASc2fbBtZ1Of97ufSDQ_XBxSJL8xgazrQud')

#Checks that the input file exists, returns an error otherwise 
def file_validifier(parser,arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    else: 
        return open(arg, 'r')

#runs IBM Emotion Analyzer on each sentence provided in captions_file
def emotion_analyser(captions_file):
    with open(captions_file) as f:
        for line in f:
            if line.strip():
                data=''.join(line.rstrip() for line in f)
                
    text= " ".join(data.split())

    tone_analysis = service.tone(
        {'text': text},
        'application/json'
    ).get_result()
    print(json.dumps(tone_analysis, indent=2))

#accepts inputfile with text to perform emotion analysis 
def main(): 
    input_file = ' '
    parser = ArgumentParser(description = "Parses caption file")
    parser.add_argument("-i", dest="inputfilename", required=True,
                    help="input file for closed captioning", metavar="CaptionsText",
                    type=lambda x: file_validifier(parser, x))
                                   
    args = parser.parse_args()
    input_file = args.inputfilename.name
    emotion_analyser(input_file)
    
    
if __name__ == "__main__":
    main()