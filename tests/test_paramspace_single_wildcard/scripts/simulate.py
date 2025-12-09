import json

with open(ismk.output[0], "w") as out:
    # convert numpy types to native python types for serialization
    json.dump({k: v.item() for k, v in ismk.params.simulation.items()}, out)