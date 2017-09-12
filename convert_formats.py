#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as et
import sys
import re
from os.path import basename
import os
import sys
import re
pattern = re.compile("^$")
rootdir = "sharedtask-data"



def mwetagprocess(input_file,filename,type):

    file2 = open(filename, 'w')
    if not os.path.exists(input_file):
        print ("input_file file does not exist", input_file)
        return 0
    print ("Exists file ", input_file)
    mwetags = []
    line_num = 0
    annotated_mwes = []
    term_closed = 0
    cont_closed = 0
    newnum = 0; lastnum = 0
    for line in open(input_file):
        if line.startswith("#"):
            continue
        line_num +=1

        if line not in ['\n', '\n\r', '\t\n']: # enumerate lines
            #print "parsemetsv:" + line
            attributes = line.split("\t")
            mwe = attributes[13]
            re_d = re.compile("(\d)")

            if not mwe.startswith("_") and ":" in mwe :
                mwe1 = re.sub(r'^[0-9]+:', r'', mwe)
                newnum = re.sub(r':.*', r'',mwe )

                type = re.sub(r'\n$', r'', mwe1)
                print "num: " + newnum + "type " + type
                if lastnum and lastnum != newnum:
                    print "</mwe>"
                print "<mwe type=\"" + type + "\" role=\"head\"" + ">"
                print line
                annotated_mwes.append(type)

            elif not mwe.startswith("_") and ":" not in mwe:
                if cont_closed == 0: # first occurence of cont
                    print "<mwe type=\"" + annotated_mwes[0] + "\" role=\"cont\">"
                    print line
                    cont_closed = 1
                elif term_closed == 0:
                    print "</mwe>"
                else:
                    print line

            elif annotated_mwes and mwe.startswith("_") and term_closed == 0:
                #discontinuous!!!wordds in between the head word
                print "</mwe>"
                print line
                term_closed = 1 # close term only before the first embedded non-mwe

            elif term_closed == 1 and  mwe.startswith("_"):
                print line

            else:
                print line

            lastnum = newnum

            mwe1 = re.sub(r'^[0-9]:', r'', attributes[13])
            mwe2 = re.sub(r';.*$', r'', mwe1)
            mwe = re.sub(r'^[0-9]$', r'CONT', mwe2)
            mwetags.append(mwe)

        else:
            print("</s>") + "\n" + ("<s>")
            file2.write("".join(mwetags))
            file2.write("\n")
            mwetags = []
            #line_num = 0
    file2.close()



def formatting(input_file, filename, lang, parseme):
    file1 = open(filename, 'w')
    if not os.path.exists(input_file):
        print ("input_file file does not exist", input_file)
        input_file = parseme
    print ("Exists file ", input_file)
    newattributes = []
    for line in open(input_file):
        if line.startswith("#"):
            continue

        if line not in ['\n', '\n\r']:
            #print "parsemetsv:" + line
            attributes = line.split("\t")
            if lang == 'MT':  # for MAltese, the forth attribute is a tag
                newattributes.append(attributes[0] + '\t' + attributes[1] + '\t' + attributes[2] + "\t" + attributes[4])
            elif lang =='HE' or lang == 'BG' or lang =='LT' or lang =='IT':
                newattributes.append(attributes[0] + '\t' + attributes[1] + '\t' + '_' + '\t' + '_')
            else:
                newattributes.append(attributes[0] + '\t'+ attributes[1] + '\t' + attributes[2] + "\t" + attributes[3])

        else:
            #print(newattributes)
            #print("\n")
            file1.write("\n".join(newattributes))
            file1.write("\n\n")
            newattributes = []

    file1.close()

def main():
    import argparse
    import subprocess
    parser = argparse.ArgumentParser()

    parser.add_argument("--annotation", type=str, help="Annotation: forms, lemmas_tags,for_TF")
    parser.add_argument("--save", type=str, help="Annotation: forms, lemmas_tags,for_TF")
    parser.add_argument("--type", type=str, help="type of annotation")
    parser.add_argument("--data", type=str, help="test.blind or train")
    args = parser.parse_args()
    from subprocess import call
    argv = sys.argv
    print ("I am here")
#    if len(argv) !=2:
#        print 'USAGE: {} <format: forms, lemmas_tags, for_TF>'.format(argv[0])
#        sys.exit(0)
    dataformat = args.annotation
    mwetagprocess("cs_40.all", "outhead100","CS")

    for root, subFolders, files in os.walk(rootdir):
        for folder in subFolders:
            #print folder
            if pattern.match(folder): #only language folders
            #print folder
                out_conllu = rootdir + "/" + folder + "/paste1_conllu_{}_{}".format(args.data, folder, dataformat)
                out_parseme = rootdir + "/" + folder + "/paste2_parseme_{}_{}".format(args.data, folder, dataformat)
                out_joinlemma = rootdir + "/" + folder + "/paste2_parseme_joinlemma_{}_{}".format(args.data, folder, dataformat)
                input_file = rootdir + "/" + folder + "/{}.conllu".format(args.data)
                parseme = rootdir + "/" + folder + "/{}.parsemetsv".format(args.data)
                all_text = "head100"
                if args.data=='test':
                    parseme = rootdir + "/" + folder + "/{}.blind.parsemetsv".format(args.data)

                if formatting(input_file, out_conllu,folder,parseme) == 0:
                    continue
                else:
                    print ("Converting ", input_file)
                    #formatting(input_file,out_conllu,folder,parseme)
                    mwetagprocess(parseme,out_parseme,dataformat)


if __name__ == "__main__":
    main()
