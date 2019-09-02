'''
Created on Mar 15, 2018

@author: Megan Chiang
'''

bfilelocation = "/scratch/RNASeq/blastp.outfmt6"

blastOutfile = open("parsedBlast.txt", "w")

with open(bfilelocation) as parsedBlast:
    for line in parsedBlast:
        fields = line.split("\t")
        transcriptID = fields[0].split("|")[0]
        isoform = fields[0].split("|")[1]
        swissprotFull = fields[1].split("|")[3]
        swissprotID = swissprotFull.split(".")[0]
        pident = fields[2]
        blastOutfile.write(transcriptID + "\t" + isoform + "\t"
                          + swissprotID + "\t" + pident + "\n")




# bfilelocation = "/scratch/RNASeq/blastp.outfmt6"
# blastfile = open(bfilelocation, 'r')
transcSwissDict = {}

def parseBlastFile():
    blastfile = openBlast()

    assert openBlast() == blastfile

    for line in blastfile:
        fields = line.split("\t")
        transcriptID = fields[0].split("|")[0]
        isoform = fields[0].split("|")[1]
        swissprotFull = fields[1].split("|")[3]
        swissprotID = swissprotFull.split(".")[0]
        transcSwissDict.update({transcriptID:swissprotID})
#         print(transcriptID + ": " + swissprotID)

def parseDEwBlast():
    DEfile = openDE()
    parsedDiffFile = open("mod08_report.txt", "w")

    for line in DEfile:
        fields = line.split("\t")
        transcriptkey = fields[0]
        spds = fields[1]
        sphs = fields[2]
        splog = fields[3]
        spplat = fields[4]

        if transcriptkey in transcSwissDict:
            proteinname = transcSwissDict[transcriptkey]
        else:
            proteinname = transcriptkey
        outputlist = [proteinname, spds, sphs, splog, spplat]
        parsedDiffFile.write("\t".join(outputlist))
        parsedDiffFile.close()

def openBlast():
    bfilelocation = "/scratch/RNASeq/blastp.outfmt6"
    blastfile = open(bfilelocation, 'r')
    return blastfile

def openDE():
    defilelocation = "/scratch/RNASeq/diffExpr.P1e-3_C2.matrix"
    DEfile = open(defilelocation, 'r')
    return DEfile

# It works
def testTranscSwiss():
    for k, v in transcSwissDict.items():
        print(k, v)

parseBlastFile()
parseDEwBlast()
# testTranscSwiss()
