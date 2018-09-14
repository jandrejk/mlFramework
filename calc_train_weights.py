from Reader import Reader
import json

def main():

    samples = "conf/global_config_2017.json"
    with open(samples,"r") as FSO:
        config = json.load(FSO)

    train_weights = {}
    for channel in ["mt","et"]:
        train_weights[channel] = getWeights(samples, channel)


        for s in config["samples"]:
            if config["samples"][s]["target"] == "none": continue


            config["samples"][s]["train_weight_scale"][channel] = train_weights[channel][config["samples"][s]["target"][channel]]

    with open(samples,"w") as FSO:
        json.dump(config, FSO, indent=2)

def getWeights(samples, channel):

    train_weights = {}
    read = Reader(channel = channel,
                  config_file = samples,
                  folds=2)

    numbers = {}
    targets = []
    

    for sample, sampleName in read.get(what = "nominal"):
        target =  read.config["target_names"][ sample[0]["target"].iloc[0] ]

        numbers[ sampleName ] = {"total": len(sample[0]) + len(sample[1]) }
        numbers[ sampleName ]["evt"] = sample[0]["event_weight"].sum() + sample[1]["event_weight"].sum()


        if numbers.get(target, None) == None:
            numbers[target] = {"evt": sample[0]["event_weight"].sum() + sample[1]["event_weight"].sum() }
            numbers[target]["total"] = len(sample[0]) + len(sample[1])
            targets.append( target )
        else:
            numbers[target]["evt"] += sample[0]["event_weight"].sum() + sample[1]["event_weight"].sum()
            numbers[target]["total"] += len(sample[0]) + len(sample[1])
        

    total = 0.
    for n in numbers:
        if n in targets: continue
        total += numbers[n]["evt"]
    # print total
    for n in numbers:
        if n not in targets: continue
        train_weights[n] = round(total / numbers[n]["evt"], 1)

        # print n, numbers[n]["total"] ,total / numbers[n]["evt"]

    return train_weights



if __name__ == '__main__':
    main()
