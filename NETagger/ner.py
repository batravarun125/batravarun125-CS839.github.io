import os
import nltk
from nltk.tag import StanfordNERTagger
from multiprocessing import Pool
import argparse


parser = argparse.ArgumentParser(description="named entity recognizer")
parser.add_argument('--dataDir', type=str, help='data directory', default='../Stage1/data/raw_copy/')
parser.add_argument('--outDir', type=str, help='output directory', default='results')
parser.add_argument('--numThreads', type=int, help='num threads', default=35)
parser.add_argument('--debugMode', action='store_true')
args = parser.parse_args()

def createString(out):

    lastPerson = False
    thisPerson = False
    textTillNow = ""
    for x in out:
        text = x[0]
        thisPerson = True if x[1]=='PERSON' else False

        if lastPerson and thisPerson:
            textTillNow = textTillNow + " " + text
        elif lastPerson and not thisPerson:
            textTillNow = textTillNow + "</name> " + text 
            lastPerson = thisPerson
        elif not lastPerson and thisPerson:
            textTillNow = textTillNow + " <name>" +  text
            lastPerson = thisPerson
        elif not lastPerson and not thisPerson:
            textTillNow = textTillNow + " " + text
    if thisPerson:
        textTillNow = textTillNow + " </name>"
    return textTillNow

def NERFile(file):
    print "{} started".format(file)
    with open(os.path.join(args.dataDir, file)) as f, open(os.path.join(args.outDir, file), "wb") as writer:
        lines = f.readlines()
        #lines = " ".join(lines)
        for line in lines:
            out = st.tag(line.split())
            if args.debugMode:
                print(out)
            out = createString(out)
            if args.debugMode:
                print(out)
            writer.write(out.encode('utf-8'))
    print "{} done".format(file)




if __name__ == "__main__":

    
    args = parser.parse_args()

    st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')

    if not args.debugMode:
        fileList = [file for file in os.listdir(args.dataDir) if os.path.isfile(os.path.join(args.dataDir, file))]
        p = Pool(args.numThreads)
        p.map(NERFile, fileList)
    else:
        NERFile("111.txt")

