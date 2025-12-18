if not ismk.resources.mem_mb == 20:
    raise ValueError("Handover of all resources did not work.")
with open(ismk.output[0], "w") as out:
    print("test", file=out)