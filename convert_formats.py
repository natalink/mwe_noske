#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import argparse
from itertools import izip
from __builtin__ import str


pattern = re.compile("^FR$")
rootdir = "data"

def num_there(s):
    return any(i.isdigit() for i in s)

def process_block(block): 
    mwe_list = []
    lemma_list = []
    for index_line, line in enumerate(block):
        if num_there(line):
            attributes = line.split()
            mwe_list.append(attributes[-1]) #last element is mwe tag from parsemetsv
            lemma_list.append(attributes[2]) #third attribute from conllu is lemma 
    
    dict_vmwe = {}
    dict_lemma = {}    
    dict_vmwe, dict_lemma = stack_vmwe_positions(mwe_list, lemma_list, dict_vmwe, dict_lemma)
    length_of_sentence = len(mwe_list)
    out_vmwe_list, out_lemma_list = form_columns(dict_vmwe, dict_lemma, length_of_sentence)
    #block = filter(None, block)
    newblock = []

    for line in block:
        if num_there(line):
            attrs = line.split()
            del attrs[-4:]
            attrs[1], attrs[0] = attrs[0], attrs[1] #swap ID and wordform (While compiling, manatee script will treat first column as word forms)
            newblock.append("\t".join(attrs))
    
    #print "BLOCK: ", newblock
    
    outblock = [ "{}\t{}\t{}".format(a, b, c) for a, b, c in  zip(newblock, out_vmwe_list, out_lemma_list) ]
    #print "\n".join(outblock)
    return outblock
    
def form_columns (dict_vmwe, dict_lemma, length_of_sentence):
    out_vmwe_list = ['_'] * length_of_sentence
    out_lemma_list = ['_'] * length_of_sentence
    for mwe_number, vmwe_tags in dict_vmwe.iteritems():
        type = vmwe_tags.split("_")[0]
        positions = vmwe_tags.split("_")[1:]
        lemma = dict_lemma[mwe_number]

        
        for ind, pos in enumerate(positions):
            if ind == 0 and out_vmwe_list[int(pos)] == '_': # :head, single 
                out_vmwe_list[int(pos)] = type + ":head"
                out_lemma_list[int(pos)] = lemma
                
            elif ind == 0 and out_vmwe_list[int(pos)] != '_':
                
                out_vmwe_list[int(pos)] =  out_vmwe_list[int(pos)] + ";" + type + ":head"
                new_lemma = out_lemma_list[int(pos)] + ";" + lemma 
                out_lemma_list[int(pos)] =  out_lemma_list[int(pos)] + ";" + lemma
                
            elif ind != 0 and out_vmwe_list[int(pos)] != '_':# ['_', '1:LVC', '_', '1;2:LVC', '_', '_', '_', '_', '2', '_']
                new_vmew = out_vmwe_list[int(pos)] + ";" + type + ":child"#
                new_lemma = out_lemma_list[int(pos)] + ";" + lemma                 
            
            else:
                out_vmwe_list[int(pos)] = type + ":child"
                out_lemma_list[int(pos)] = lemma
                

    return out_vmwe_list, out_lemma_list
            
           
#########Given mwe and lemma attribute lists returns the positions. Output: mwe_list: {'1': 'LVC_3_5'} lemma_list:{'1': 'il_de'} ############
def stack_vmwe_positions(mwe_list, lemma_list, dict_vmwe, dict_lemma):
   
    for ind, mwe in enumerate(mwe_list):
        if ";" in mwe:
            multiple_mwes = mwe.split(";")
            for mul_mwe in multiple_mwes:
                if ":" in mul_mwe:
                    number_mwe, type_mwe = mul_mwe.split(":")
                    position_type = type_mwe + "_" + str(ind)
                    dict_vmwe[number_mwe] = position_type
                    lemma = lemma_list[ind]
                    dict_lemma[number_mwe] = lemma
                else: # ['_', '1:LVC', '_', '1;2:LVC', '_', '_', '_', '_', '2', '_'] quick_ugly_hack!! need to make some recursion instead.
                    print "THIS MWE needs special treatment", mul_mwe
                    if mul_mwe in dict_vmwe:
                        current_value = dict_vmwe.get(mul_mwe)
                        new_value = current_value + "_" + str(ind)
                        dict_vmwe.update({mul_mwe: new_value})
                        current_lemma = dict_lemma.get(mul_mwe)
                        new_lemma = current_lemma + "_" + lemma_list[ind]
                        dict_lemma.update({mul_mwe: new_lemma})
                
        elif ":" in mwe and not ";" in mwe:
            number_mwe, type_mwe = mwe.split(":")
            position_type = type_mwe + "_" + str(ind)
            dict_vmwe[number_mwe] = position_type
            lemma = lemma_list[ind]
            dict_lemma[number_mwe] = lemma

                                        
        elif mwe.isdigit():
            if mwe in dict_vmwe:
                current_value = dict_vmwe.get(mwe)
                new_value = current_value + "_" + str(ind)
                dict_vmwe.update({mwe: new_value})
                current_lemma = dict_lemma.get(mwe)
                new_lemma = current_lemma + "_" + lemma_list[ind]
                dict_lemma.update({mwe: new_lemma})
        
    #print dict_vmwe
    #print dict_lemma
    return dict_vmwe, dict_lemma
        

def mwetagprocess(input_conllu, parsemetsv):
    
    vert_out = os.path.splitext(input_conllu)[0]+'.vert'
    print (parsemetsv, vert_out)
    file2 = open(vert_out, 'w')
    if not os.path.exists(input_conllu):
        print ("input_file file does not exist", input_conllu)
        return 0
    print ("Exists file ", input_conllu)    
    file2.write("<doc>\n")
    for block in read_blocks(input_conllu, parsemetsv):
        outblock = process_block(block)

        file2.write("<s>\n")
        file2.write("\n".join(outblock))
        file2.write("\n</s>\n")
        
    file2.write("</doc>")
    file2.close
   
def read_blocks(input_conllu, parsemetsv):    # function stolen from SO
    with open(input_conllu) as file_conllu, open(parsemetsv) as file_parsemetsv: 
        empty_lines = 0
        blocks = []

        for line, line_parsemetsv in izip(file_conllu, file_parsemetsv):
            #print "LINE: ", line, line_parsemetsv
        # Check for empty/commented lines
            if not line or line.startswith('#'):
            #    print "if not line or line.startswith('#') or line in ['', '\n', '\n\r', '\t\n']:", line
            # If 1st one: new block
                if empty_lines == 0:
                    blocks.append([])
                empty_lines += 1
        # Non empty line: add line in current(last) block
            else:

                empty_lines = 0
                line = line.strip()
                line_parsemetsv = line_parsemetsv.strip()                
                blocks[-1].append(line+"\t"+line_parsemetsv)
                
    #blocks = filter(None, blocks)
    return blocks
        

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="test.blind or train")

    for root, subFolders, files in os.walk(rootdir):
        for lang_folder in subFolders:
            if pattern.match(lang_folder): #only language folders
                conllu = rootdir + "/" + lang_folder + "/60.train.conllu"
                parsemetsv = rootdir + "/" + lang_folder + "/60.train.parsemetsv"
                
                mwetagprocess(conllu, parsemetsv)


if __name__ == "__main__":
    main()
