assert ismk.input.get("sort", "missing") == "missing"

with open(ismk.output[0], "w") as out:
    print(1, 2, 3, file=out)
