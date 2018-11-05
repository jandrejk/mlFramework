from Reader import Reader
from Tools.Datacard.produce import Datacard, makePlot
import copy
import pandas
import json
import sys
import os
import argparse
import cPickle
import subprocess as sp
import multiprocessing as mp

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel' ,choices = ['mt','et','tt'], default = 'mt')
    parser.add_argument('-m', dest='model',   help='ML model to use' ,choices = ['keras','xgb'],  default = 'keras')
    parser.add_argument('-t', dest='train',   help='Train new model' , action='store_true')
    parser.add_argument('-s', dest='short',   help='Do !!NOT!! predict shapes' , action='store_true')
    args = parser.parse_args()

    print "---------------------------"
    print "Running over {0} samples".format(args.channel)
    print "Using {0}".format(args.model)
    if args.train:
        print "Training new model"
    if args.short:
        print "Not predicting shape templates."
    print "---------------------------"

        
    run(samples = "conf/global_config_2016.json",
        channel=args.channel,
        use = args.model,
        train = args.train,
        short = args.short
          )

def run(samples,channel, use, train,short, preprocess_chain = []):

    if use == "xgb":
        from XGBModel import XGBObject as modelObject
        parameters = "conf/parameters_xgb.json"

    if use == "keras":
        from KerasModel import KerasObject as modelObject
        parameters = "conf/parameters_keras.json"


    read = Reader(channel = channel,
                  config_file = samples,
                  folds=2)

    target_names = read.config["target_names"]
    variables = read.config["variables"]
    if not os.path.exists("models"):
        os.mkdir("models")

    modelname = "models/{0}.{1}".format(channel,use)
    scaler = None

    if train:
        print "Training new model"
        print "Loading Training set"
        trainSet = read.getSamplesForTraining()

        print "Fit Scaler to training set...",
        scaler = trainScaler(trainSet, variables )

        print " done. Dumping for later."
        with open("models/StandardScaler.{0}.pkl".format(channel), 'wb') as FSO:
            cPickle.dump(scaler, FSO , 2)
        trainSet = applyScaler(scaler, trainSet, variables)

        model = modelObject( parameter_file = parameters,
                             variables=variables,
                             target_names = target_names )
        model.train( trainSet )
        model.save(modelname)

    else:
        if os.path.exists("models/StandardScaler.{0}.pkl".format(channel) ):
            print "Loading Scaler"
            with open( "models/StandardScaler.{0}.pkl".format(channel), "rb" ) as FSO:
                scaler = cPickle.load( FSO )

        print "Loading model and predicting."
        model = modelObject( filename = modelname )



    predictions = {}
    print "Predicting samples"
    for sample, sampleName in read.get(what = "full", add_jec = not short, for_prediction = True):
        if "data" in sampleName:
            sandbox(channel, model, scaler, sample, variables, "NOMINAL_ntuple_Data")
        elif "full" in sampleName:
            sandbox(channel, model, scaler, sample, variables,  "NOMINAL_ntuple_" + sampleName.split("_")[0] )
        else:
            splName = sampleName.split("_")
            sandbox(channel, model, scaler, sample, variables,  "_".join(splName[1:])+"_ntuple_" + sampleName.split("_")[0] )

    if not short:
        print "Predicting TES shapes"
        for sample, sampleName in read.get(what = "tes", for_prediction = True):
            sandbox(channel, model, scaler, sample, variables, sampleName  )





    Datacard.use_config = "datacardConf"
    D = Datacard(channel, "predicted_prob", False, False)
    D.create(use)
    makePlot(channel, "predicted_prob", use)

def sandbox(channel, model, scaler, sample, variables, outname):
    # needed because of memory management
    # iterate over chunks of sample and do splitting on the fly
    first = True
    for part in sample:
        part["evt"] = part["evt"].astype('int64')
        folds = [part.query( "evt % 2 != 0 " ).reset_index(drop=True), part.query( "evt % 2 == 0 " ).reset_index(drop=True) ]
        addPrediction(channel, model.predict( applyScaler(scaler, folds, variables) ), folds, outname, new = first )
        first = False

def addPrediction(channel,prediction, df, sample, uncert = {}, new = True):

    for i in xrange( len(df) ):
        for c in prediction[i].columns.values.tolist():
            df[i][c] =  prediction[i][c]
            for jec in uncert:
                df[i][c+jec] = uncert[jec][i][c]

        if i == 0 and new: mode = "w"
        else: mode = "a"
        df[i].to_root("{0}/{1}-{2}.root".format("predictions",channel, sample), key="TauCheck", mode = mode)

def trainScaler(folds, variables):
    from sklearn.preprocessing import StandardScaler

    total = pandas.concat( folds, ignore_index = True ).reset_index(drop=True)
    Scaler = StandardScaler()
    Scaler.fit( total[ variables ] )


    return Scaler

def applyScaler(scaler, folds, variables):
    if not scaler: return folds
    newFolds = copy.deepcopy(folds)
    for fold in newFolds:
        fold[variables] = scaler.transform( fold[variables] )
    return newFolds


if __name__ == '__main__':
    main()
