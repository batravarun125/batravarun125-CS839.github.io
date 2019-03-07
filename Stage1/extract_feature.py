import pandas as pd
import string
import sys
df = pd.read_csv(sys.argv[1],delimiter='_')
var = "test"
if sys.argv[1]=='preprocessed_data_train.csv':
    var="train"
def insert_csv_col(header,value):
    df.insert(len(df.columns),header,value)
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

if __name__ == '__main__':
    insert_csv_col("POST_VERB_DISCTANCE",100)
    insert_csv_col("PRE_TITLE", False)
    insert_csv_col("PRE_ARTICLE_DISTANCE", False)
    insert_csv_col("LOCATION_BASED", False)
    insert_csv_col("PRE_POSITION_DISTANCE", 100)
    insert_csv_col("EXTRAS", False)
    insert_csv_col("PRE_POST_CAPITAL", False)
    insert_csv_col("POST_APOSTROPHE", False)
    insert_csv_col("POST_PREPOSITION", False)
    insert_csv_col("RELATIONSHIP", False)
    insert_csv_col("POST_SAY_SYNONYM", False)
    insert_csv_col("PRE_SAY_SYNONYM", False)
    insert_csv_col("POSITION", False)
    insert_csv_col("COUNTRY", False)

    verbs_file = open('./specials/verbs.txt')
    stopwords_file = open('./specials/stopwords.txt')
    prepositions_file=open('./specials/prepositions.txt')
    articles_file=open('./specials/articles.txt')
    prefixes_file = open('./specials/prefixes.txt')
    saySynonmys_file = open('./specials/saySynonyms.txt')
    relationships_file = open('./specials/relations.txt')
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



    for j in range(len(df)):
        sfile = open('./data/raw/' + df.loc[j]['filename'][-7:])
        ls = sfile.read().split()
        start = df.loc[j]['start_ind']
        end = df.loc[j]['end_ind']
        instance = df.loc[j]["Tokens"]

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
                df.at[j,"POST_VERB_DISTANCE"]=postring.index(i)
                break

        df.at[j, "PRE_TITLE"] = prefixMatch(instance)
        df.at[j, "POST_APOSTROPHE"] = postApostropheMatch(instance)

        if postword in prepositions:
            df.at[j,"POST_PREPOSITION"]=True

        if preword in articles:
            df.at[j,"PRE_ARTICLE_DISTANCE"]= True

        if postword.lower() in saySynonmys:
            df.at[j,"POST_SAY_SYNONYM"]= True

        if preword.lower() in saySynonmys:
            df.at[j,"PRE_SAY_SYNONYM"]= True

        if postword.lower() in relationships:
            df.at[j,"RELATIONSHIP"]= True

        for word in prestring:
            if word in verbs:
                df.at[j,"PRE_VERB_DISTANCE"]=len(prestring)- prestring.index(word)

        for word in prestring:
            if word in positions:
                df.at[j,"PRE_POSITION_DISTANCE"]=len(prestring)- prestring.index(word)
                break

        if instance in positions:
            df.at[j,"POSITION"]=True

        if instance in country:
            df.at[j,"COUNTRY"]=True

        for word in prestring:
            if word in locations:
                df.at[j,"LOCATION_BASED"] = True

        extra_positives = ['himself','herself','themselves','who']
        for k in postring:
            if k in extra_positives:
                df.at[j, "EXTRAS"] = True

        if(len(prestring)>0):
            if prestring[len(prestring)-1][0] in string.ascii_uppercase:
                    df.at[j,"PRE_POST_CAPITAL"] = True
        if(len(postring)>0):
            if postring [0][0] in string.ascii_uppercase:
                    df.at[j, "PRE_POST_CAPITAL"] = True

    df.to_csv("input_features" + var +".csv", ',', False)
