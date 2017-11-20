import json

all_features = ["VerbToTheLeft", "VerbToTheRight", "UnitFoundInQuestion", "BestQuantUnitMatchInQuestion", "MultipleQuantUnitBestMatchInQuestion",
                "ExactMatchUnit", "OtherPairExactMatchUnit","NoMatchWithOtherQuantUnits","BestMatchAmongQuantUnit",
                "Two_quantities"]

with open("RelFeat.json", 'r') as f:
    read = json.load(f)
    for elem in read:
        print "index",elem['index']
        print "interest", elem["interest"]
        for feat in all_features:
            if feat in elem['feature']:
                print feat, 1
            else:
                print feat, 0
        print  

