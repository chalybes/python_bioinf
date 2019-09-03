'''
Created on Apr 6, 2018

This script makes 2 objects, blastParser and
matrixParser for use later in a list comprehension.
Ultimately the list comprehension will give
you the protein names of the genes found to be
differentially expressed during diauxic shift,
heat shock, growth, and plateau.

@author: Megan Chiang
'''

class blastParser(object):

    def __init__(self):

        self.transcSwissDict = {}

        with open("/scratch/RNASeq/blastp.outfmt6") as file:
            listoffields = [lines.rstrip().split("\t") for lines in file]  # Makes a list of all lines from file
            self.listoftranscriptID = [fields[0].split("|")[0] for fields in listoffields] # Grabs all transcript ID out of file list
            listofcompleteswissprotID = [fields[1].split("|")[3] for fields in listoffields] # Grabs all complete SwissProt IDs including ver. number
            self.listofswissprotID = [protid.split(".")[0] for protid in listofcompleteswissprotID] # Split the complete SwissProt ID to get a list of core IDs without versions
            self.listofpident = [fields[2] for fields in listoffields] # Get the list of identity percentage


class matrixParser(object):

    def __init__(self, blastObj, DElines):

        blastdata = blastObj
        DEFields = DElines.rstrip("\n").split("\t")

        # Checks if the transcript ID from the gene expression file
        # exists in the blastObj (which is the Blastp output file)
        if DEFields[0] in blastdata.transcSwissDict:
            self.protein = blastdata.transcSwissDict[DEFields[0]]
        else:
            self.protein = DEFields[0]

        # Set the rest of the attributes
        self.diauxicshift = DEFields[1]
        self.heatshock = DEFields[2]
        self.loggrowth = DEFields[3]
        self.plateau = DEFields[4]

    # Can't return anything in __init__, so this method returns
    # the set Matrix attributes as a tuple
    def makeAttrTuple(self):
        return (self.protein, self.diauxicshift, self.heatshock, self.loggrowth, self.plateau)


def checkPercentIdent(blastObj):
    blastlists = blastObj

    # Get the index of all transcripts with pident of < 95
    listoflowpident = [i for i,v in enumerate(blastlists.listofpident) if float(v) < 95]

    # Filter the original list of transcripts using listoflowpident,
    # the indices in listsoflowpident correspond to the indices of the transcript
    # that need to be removed. The same need to be done to SwissProt IDs
    filtered_transcript = [i for j, i in enumerate(blastlists.listoftranscriptID) if j not in listoflowpident]
    filtered_swissprot = [i for j, i in enumerate(blastlists.listofswissprotID) if j not in listoflowpident]

    # Zip the 2 filtered lists together to make the dict
    blastlists.transcSwissDict = dict(zip(filtered_transcript, filtered_swissprot))


# Process the tuple with formatting
def tupleToTab(atuple):
    return "\t".join(atuple)

testBlast = blastParser()
checkPercentIdent(testBlast)
DEfile = open("/scratch/RNASeq/diffExpr.P1e-3_C2.matrix")

# Call the class matrixParser() in list comprehension in order to pass DEfile line by line into matrixParser object
DEtuples = [matrixParser(testBlast, DElines).makeAttrTuple() for DElines in DEfile.readlines()]

DEfile.close()

listofTabbedDE = map(tupleToTab, DEtuples)
parsedDEfile = open("DEresults_matchedBlast.txt", "w")
parsedDEfile.write("\n".join(listofTabbedDE))
parsedDEfile.close()
