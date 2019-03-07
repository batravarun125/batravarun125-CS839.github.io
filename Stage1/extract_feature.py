import pandas as pd
import string
import sys
df = pd.read_csv(sys.argv[1])
var = "test"
if sys.argv[1]=='preprocessed_data_train.csv':
    var="train"
df.insert(len(df.columns), "PRE_DIST_VERB", 100)
df.insert(len(df.columns), "POST_DIST_VERB",100)
df.insert(len(df.columns), "PrecedingTitle", False)
df.insert(len(df.columns), "PRE_DIST_FROM_THE", False)
df.insert(len(df.columns), "PRE_DIST_FROM_POSITION", 100)
df.insert(len(df.columns), "NEGATIVE_FEATURE", False)
df.insert(len(df.columns), "POSITIVE_FEATURE", False)
df.insert(len(df.columns), "Surrounding_Caps", False)
df.insert(len(df.columns), "Apostrophe", False)
df.insert(len(df.columns), "POST_IS_PREPOSITION", False)
df.insert(len(df.columns), "RELATIONSHIP", False)
df.insert(len(df.columns), "POST_IS_SPEAK_VERB", False)
df.insert(len(df.columns), "PRE_IS_SPEAK_VERB", False)
df.insert(len(df.columns), "INSTANCE_IS_POSITION", False)
df.insert(len(df.columns), "INSTANCE_IS_COUNTRY", False)

verbs_file = open('./specials/verbs.txt')
stopwords_file = open('./specials/stopwords.txt')
prepositions_file=open('./specials/prepositions.txt')
articles_file=open('./specials/articles.txt')
prefixes_file = open('./specials/prefixes.txt')
saySynonmys_file = open('./specials/saySynonmys.txt')
relationships_file = open('./specials/relationships.txt')
positions_file = open('./specials/positions.txt')
country_file = open('./specials/country.txt')
locations_file = open('./specials/locations.txt')

verbs = verbs_file.read().split()
stopwords = stopwords_file.read().split()
prepositions=prepositions_file.read().split()
articles=articles_file.read().split()
prefixes=prefixes_file.read().split()
saySynonmys=saySynonmys_file.read().split()
relationships = relationships_file.read().split()
positions = positions_file.read().split()
country = country_file.read().split()
locations = locations_file.read().split()

def prefixMatch(instance):
    l = instance.split(" ")
    if l[0] in prefixes or (l[0] + ".") in prefixes:
        return True
    return False
def postApostropheMatch(instance):
    l = instance.split(" ")
    val = l[-1]
    if val[-1] == "\'" or val[-2:] == "\'s":
        return True
    return False


for j in range(len(df)):
    sfile = open('./data/raw_copy/' + df.loc[j]['filename'][-7:])
    ls = sfile.read().split()
    start = df.loc[j]['start']
    end = df.loc[j]['end']
    instance = df.loc[j]["Word"]

    if start>5:
        prestring = ls[start-5:start]
        if '.' in prestring:
            prestring = prestring[prestring.index('.')+1:]
    else:
        prestring = ls[0:start]
        if '.' in prestring:
            prestring = prestring[prestring.index('.')+1:]
    if end< len(ls)-5:
        postring = ls[end+1:end + 5]
        if '.' in postring:
            postring = postring[0:postring.index('.')]
    else:
        postring = ls[end+1:len(ls)-1]
        if '.' in postring:
            postring = postring[0:postring.index('.')]

    if start>1:
        preword = ''.join(ls[start-1:start])
    else:
        preword = ''.join(ls[0:start])

    if end< len(ls)-1:
        postword = ''.join(ls[end+1:end+2])

    else:
        postword = ''.join(ls[end+1:len(ls)-1])

    for i in postring:
        if i in verbs:
            df.at[j,"POST_DIST_VERB"]=postring.index(i)
            break

    df.at[j, "PrecedingTitle"] = prefixMatch(instance)
    df.at[j, "Apostrophe"] = postApostropheMatch(instance)

    if postword in prepositions:
        df.at[j,"POST_IS_PREPOSITION"]=True

    if preword in articles:
        df.at[j,"PRE_DIST_FROM_THE"]= True

    if postword.lower() in saySynonmys:
        df.at[j,"POST_IS_SPEAK_VERB"]= True

    if preword.lower() in saySynonmys:
        df.at[j,"PRE_IS_SPEAK_VERB"]= True

    if postword.lower() in relationships:
        df.at[j,"RELATIONSHIP"]= True

    for word in prestring:
        if word in verbs:
            df.at[j,"PRE_DIST_VERB"]=len(prestring)- prestring.index(word)

    for word in prestring:
        if word in positions:
            df.at[j,"PRE_DIST_FROM_POSITION"]=len(prestring)- prestring.index(word)
            break

    if instance in positions:
        df.at[j,"INSTANCE_IS_POSITION"]=True

    if instance in country:
        df.at[j,"INSTANCE_IS_COUNTRY"]=True

    for word in prestring:
        if word in locations:
            df.at[j,"NEGATIVE_FEATURE"] = True

    extra_positives = ['himself','herself','themselves','who']
    for k in postring:
        if k in extra_positives:
            df.at[j, "POSITIVE_FEATURE"] = True

    if(len(prestring)>0):
        if prestring[len(prestring)-1][0] in string.ascii_uppercase:
                df.at[j,"Surrounding_Caps"] = True
    if(len(postring)>0):
        if postring [0][0] in string.ascii_uppercase:
                df.at[j, "Surrounding_Caps"] = True

df.to_csv("input_features" + var +".csv", sep=',', index=False)