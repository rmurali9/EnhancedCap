from bs4 import BeautifulSoup
import sys 
from argparse import ArgumentParser
import os.path

#Checks that the input file exists, returns an error otherwise 
def file_validifier(parser,arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    else: 
        return open(arg, 'r')

#parses the input file to obtain the caption texts 
#TODO: parse the beginning and end times for texts 
def parse_captions_xml(captions_file, output_file):
    with open (captions_file) as fp: 
        soup = BeautifulSoup(fp,"xml")
    
    caption_body = soup.body
    caption_lines = caption_body.find_all('p')
    caption_text = ' '

    for caption in caption_lines:
        caption_text = "".join((caption_text, caption.get_text()))
    
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