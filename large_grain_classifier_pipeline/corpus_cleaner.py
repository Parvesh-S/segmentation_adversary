import csv
import requests
import xml.etree.ElementTree as ET
import glob
import os
import codecs

path = '/af5/mw3yg/nlp/policy_data_gen/opp_115/corpus/'
outfile = codecs.open("cleaned_policy_corpus.txt","a+","utf-8")
'''
Idea:
Grab text from xml files section by section and
if the grabbed section seems incomplete, mark that it 
needs to be appended to the next section. 
Once marked, append it and move on.
'''
is_complete = True

for filename in glob.glob(os.path.join(path, '*.xml')):
    data = ET.parse(filename)
    root = data.getroot()
    
    for section in root.findall('SECTION'):
        content = section.find('SUBTEXT').text
        #print('%s' % (content))
        #print('-------------------------------')
        data = content.split("\n")
        #print (data)
        data[:] = [x for x in data if x != ""]
        #print (data)
        inter_str = ""
        for line in data:
            print(" Inter_str: " + inter_str)
            print (line)
            append_needed = input("DOES THE ABOVE SECTION NEED APPENDING? REPLY (t/f)...")
            if append_needed == "f":
                is_complete = True
                if inter_str == "":
                    print("WRITING TO FILE...")
                    outfile.write(line+' '+' \n')
                    outfile.write('\n')
                else:
                    print("WRITING TO FILE...")
                    outfile.write(inter_str)
                    inter_str = ""
                    outfile.write(' \n')
            else:
                inter_str += line
                print("success")
            


            
        #content.encode('utf-8', 'ignore')
        #outfile.write(unicode(content))               
