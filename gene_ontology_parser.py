'''
Created on Mar 20, 2018

This script will only grab you the relevant
chunks of a gene ontology file
(name, explanation of functions, related genes).

@author: Megan Chiang
'''

import re

GODict = {}

def openGOFile():
    GOfilelocation = "/scratch/go-basic.obo"
    GOfile = open(GOfilelocation, 'r')
    return GOfile


def processGO():

    GOfileraw = openGOFile()
    GOfile = GOfileraw.read()

    GO_records = re.split(r'(?=Term*)', GOfile)

    return GO_records


def fieldgrabber():

    # GOchunks is a list
    GOchunks = processGO()

    # Have to convert GOchunks to string because re.finditer only works on strings
    GOlongstring = ''.join(GOchunks)

    # This pattern works for almost every case, though I don't know why sometimes it picks up an alt_id randomly
    pattern = re.compile(r'(id:\s\w+\W+\d+\n)(name:\s.+?\n)(namespace:\s.+?)def:\s.+?((is_a:\sGO:\d+.+?\n){1,})', re.DOTALL)

    # User re's finditer method to parse through the extremely long GO file string
    for m in re.finditer(pattern, GOlongstring):
        # These are all the capture groups for the target fields:
        # id, name, namespace, and is_a(s)
        fullid = m.group(1)
        name = m.group(2)
        namesumm = m.group(3)
        is_a = m.group(4)

        # Split the strings because we don't need the starting words
        # i.e. id: , name: , namespace: , is_a:
        goid = fullid.split(":", 1)[1]
        summsplit = namesumm.split(":", 1)[1]
        namesplit = name.split(":", 1)[1]

        # There may be more than 1 is_a for some records, if so, the is_a(s)
        # beyond the first one would need to be processed
        isasplit = is_a.split("is_a: ")
        # Add tab spaces for each element in the list of is_a(s)
        isasplit = ['\t{0}'.format(elem) for elem in isasplit]
        # Concat all is_a(s) into a string in order to combine it with name
        isasplitconcat = ''.join(isasplit)

        # Concat GOID with namespace to form the key for dict
        # Concat name with is_a to form the value for dict
        key = goid.rstrip() + "\t" + summsplit
        value = namesplit + isasplitconcat

        # Store everything into dict
        GODict.update({key:value})


def checkGODict():
    for k, v in GODict.items():
        print(k + "\t" + v)


fieldgrabber()
checkGODict()
