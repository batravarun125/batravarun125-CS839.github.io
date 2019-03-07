import pandas as pd
import os, sys
import argparse


parser = argparse.ArgumentParser(description = 'removing not relevant labels')
parser.add_argument('--notRemoveVerbs', action='store_true')
parser.add_argument('--notRemoveCountries', action='store_true')
parser.add_argument('--notRemoveStopWords', action='store_true')
parser.add_argument('--notRemoveDigits', action='store_true')
#parser.add_argument('--notRemoveStopWords', action='store_true')

parser.add_argument('--dataFile', type=str, help="data file")
parser.add_argument('--verbFile', type=str, help='verbs ', default='../Corpus/verbs.txt')
parser.add_argument('--countryFile', type=str, help = 'country file', default='../Corpus/countries.txt')
parser.add_argument('--prepositionsFile', type=str, help = 'prep file', default='../Corpus/prepositions.txt')
parser.add_argument('--stopwordsFile', type=str, help='stopwords file', default='../Corpus/stopwords.txt')

parser.add_argument('--outFile', type=str, help='outFile path', default='results/PreProcessed.csv')

def readFile(file, lower=True):
    
    if lower:
        return [x.strip().lower() for x in open(file).readlines()]
    else:
        return [x.strip() for x in open(file).readlines()]


if __name__ == '__main__':


    args = parser.parse_args()
    # only filter on `Tokens` col
    data = pd.read_csv(args.dataFile)
    #Create a DataFrame
    #d = {
    #        'Tokens':['play','is','india','jack','raghu','Cathrine',
    #                'Alisa','Bobby','kum2ar','Alisa','Alex','Cathrine'],
    #        'Age':[26,24,23,22,23,24,26,24,22,23,24,24],
    #  
    #        'Score':[85,63,55,74,31,77,85,63,42,62,89,77]}
 
    #data = pd.DataFrame(d,columns=['Tokens','Age','Score'])
    
    totalRowsRemoved = 0
    
    if not args.notRemoveVerbs:

        print("Removing Versbs")
        #load verbs
        verbs = readFile(args.verbFile)
        initRow = data.shape[0]
        data = data[~data['Tokens'].isin(verbs)]
        finRow = data.shape[0]
        print("VERBS: Removed {} rows".format(initRow-finRow))
        totalRowsRemoved += initRow - finRow

    if not args.notRemoveCountries:
        print("Removing Countries")
        countries = readFile(args.countryFile)
        initRow = data.shape[0]
        data = data[~data['Tokens'].isin(countries)]
        finRow = data.shape[0]
        print('COUNTRIES: Removed {} rows'.format(initRow-finRow))
        totalRowsRemoved += initRow - finRow


    if not args.notRemoveStopWords:
        print("Removing Stop Words")
        stopwords = readFile(args.stopwordsFile)
        initRow = data.shape[0]
        data = data[~data['Tokens'].isin(stopwords)]
        finRow = data.shape[0]
        print("STOPWORDS: Removed {} rows".format(initRow-finRow))
        totalRowsRemoved += initRow - finRow

    if not args.notRemoveDigits:
        print("Removing Names with Digits")
        initRow = data.shape[0]
        data = data[~data['Tokens'].str.contains(r'[0-9]')]
        finRow = data.shape[0]
        print("DIGITS: Removed {} rows".format(initRow - finRow))
        totalRowsRemoved += initRow - finRow
        
    
    print('TOTAL: {} rows removed'.format(totalRowsRemoved))

    data.to_csv(args.outFile, index=False)
