'''
Created on Apr 6, 2018

This Python script will make a gene ontology
parser as an object for later use instead of simply
parsing a GO file for you. 

AKA this is just a class obj of gene_ontology_parser.py

@author: Megan Chiang
'''

import re

class parseGO(object):

    def __init__(self, record):

        # Initialize dictionary for GO terms within this class
        self.GODict = {}

        fullid_search = re.search(r"id:\s(GO:\d+)\n", record, re.DOTALL)
        name_search = re.search(r"name:\s(.+?)\n", record, re.DOTALL)
        namespace_search = re.search(r"namespace:\s(.*?)\n", record, re.DOTALL)
        is_a_search = re.findall(r"is_a:\s(GO:\d+.*?)\n", record, re.DOTALL)

        # If there is an ID, then assign all captures appropriately
        if fullid_search:

            self.id = fullid_search.group(1)
            self.name = name_search.group(1)
            self.namespace = namespace_search.group(1)

            # If is_a exists, then assign is_a as a class object
            if is_a_search:
                self.is_a = is_a_search
            else:
                self.is_a = None
        else:
            self.id = None

    # Output all fields by printing to console
    def print_all(self):
        if self.id:
            print(self.id)
            print(self.name)
            print(self.namespace)

            if self.is_a:
                print(str(self.is_a) + "\n")

    # Function to fill up the dictionary
    def makeGODict(self):

        if self.id:
            key = str(self.id) + "\t" + str(self.namespace) + "\n"

            if self.is_a:
                value = str(self.name) + "\n" + str(self.is_a)
            else:
                value = str(self.name) + "\n"

        self.GODict.update({key:value})

    # Output the contents of the dictionary to text file
    def outputGODict(self):

        for key,value in self.GODict.items():
            filecontent = key + value + "\n"
            print(filecontent)
            with open("parsed_gene_ontology_output.txt", "w") as file:
                file.write(filecontent)


# Function to split the original GO file into individual records
def splitEntriesByTerms(obofile):
    with open(obofile) as f:
        records = f.read()
        splitrecords = re.findall(r'\n\[Term\]\n(.+?\n{1,})\n', records, re.DOTALL)

        for GO_record in splitrecords:
            GOentry = parseGO(GO_record)
            GOentry.makeGODict()
            GOentry.outputGODict()
#             GOentry.print_all()

splitEntriesByTerms("/scratch/go-basic.obo")
