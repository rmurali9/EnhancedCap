from __future__ import print_function
from bs4 import BeautifulSoup

import sys 

from argparse import ArgumentParser

import os.path

import csv


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

     iam_apikey= key)



#Checks that the input file exists, returns an error otherwise 

def file_validifier(parser,arg):

    if not os.path.exists(arg):

        parser.error("The file %s does not exist" % arg)

    else: 

        return open(arg, 'r')



#runs IBM Emotion Analyzer on each sentence provided in captions_file

def emotion_analyser(text):

    tone_analysis = service.tone(

        {'text': text},

        'application/json'

    ).get_result()
    return tone_analysis

    #return(json.dumps(tone_analysis, indent=2))





#Checks that the input file exists, returns an error otherwise 

def file_validifier(parser,arg):

    if not os.path.exists(arg):

        parser.error("The file %s does not exist" % arg)

    else: 

        return open(arg, 'r')

#looks up the emotion and generates te adequate style
def emo_capt(emo):
 style = "0"
 if emo["document_tone"]["tones"]:
    if emo["document_tone"]["tones"][0]['tone_id'] == 'anger':
	        style = "1"
    elif emo["document_tone"]["tones"][0]['tone_id'] == 'joy':
            style = "2"
    elif emo["document_tone"]["tones"][0]['tone_id'] == 'fear':
            style = "3"
    elif emo["document_tone"]["tones"][0]['tone_id'] == 'sadness':
	        style = "4"
    elif emo["document_tone"]["tones"][0]['tone_id'] == 'disgust':
	        style = "5"
 else:
    style = "0"
 return style

# checks the emotional content and sets style according to score
def emo_capt_scorebased(emo):
 style = "0"
 if emo["document_tone"]["tones"]:
   if emo["document_tone"]["tones"][0]['tone_id'] == 'anger' and emo["document_tone"]["tones"][0]['score'] > 0.9:
            style = "1"
   elif emo["document_tone"]["tones"][0]['tone_id'] == 'joy' and emo["document_tone"]["tones"][0]['score'] > 0.9:
            style = "2"
   elif emo["document_tone"]["tones"][0]['tone_id'] == 'fear' and emo["document_tone"]["tones"][0]['score'] > 0.9:
            style = "3"
   elif emo["document_tone"]["tones"][0]['tone_id'] == 'sadness' and emo["document_tone"]["tones"][0]['score'] > 0.9:
            style = "4"
   elif emo["document_tone"]["tones"][0]['tone_id'] == 'disgust' and emo["document_tone"]["tones"][0]['score'] > 0.9:
            style = "5"
 else:
   style = "0"
 return style

#parses the input file to obtain the caption texts 

#TODO: parse the beginning and end times for texts 

def parse_captions_xml(captions_file, output_file):

    with open (captions_file) as fp: 

        soup = BeautifulSoup(fp,"xml")

    """
	to see the output of caption_lines
	check if time of each caption can be extracted
	check if the jason elements can be obtained seperately
	to write the captoion with added style into a ttml output file with the xml strat tags and end tags
	"""

    caption_body = soup.body

    caption_lines = caption_body.find_all('p')

    caption_text = '<tt xmlns="http://www.w3.org/2006/04/ttaf1" xmlns:tts="http://www.w3.org/2006/04/ttaf1   <head>     <styling>      <style id="0" tts:fontSize="14" tts:textAlign="center" tts:wrapOption="wrap"/> <style id ="1" tts:fontsize="40" tts:textAlign= "center" tts:color= "red"/> <style id ="2" tts:fontsize="20" tts:textAlign= "center" tts:color= "yellow"/> <style id ="3" tts:fontsize="8" tts:textAlign= "center" tts:color= "white"/> <style id ="4" tts:fontsize="10" tts:textAlign= "center" tts:color= "blue"/> <style id ="5" tts:fontsize="30" tts:textAlign= "center" tts:color= "disgust"/>    </styling>  </head> <body> <div xml:lang="en">'
        

    for caption in caption_lines:
      emo = emotion_analyser(caption.get_text())
      style = emo_capt(emo)
      print(style)
      begin = caption['begin']
      end = caption['end']
      caption_text = caption_text+ '<p begin = '+begin+ 'end = '+end+ 'style = '+ style +'>'+caption.get_text()+'<br/></p>'
    caption_text = caption_text + '</div>   </body> </tt>'
    

    #writes to output file specified by user 

    f1=open(output_file, 'w+')

    f1.write(caption_text)

    f1.close()

      

#obtains an input and output file from user, provides parsed captions text      

def main(): 

    input_file = ' '

    output_file = ' '

    parser = ArgumentParser(description = "Parses caption file")

    parser.add_argument("-i", dest="inputfilename", required=True,

                    help="input file for closed captioning", metavar="CaptionsFile",

                    type=lambda x: file_validifier(parser, x))

                    

    parser.add_argument("-o", dest="outputfilename", required=True,

                help="output file for parsed information", metavar="OutputFile")

    args = parser.parse_args()

    input_file = args.inputfilename.name

    output_file = args.outputfilename

    parse_captions_xml(input_file, output_file)

    

    

if __name__ == "__main__":

    main()
