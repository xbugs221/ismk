from ismk.script import ismk


def _write_output():
    with open(ismk.output[0], "w") as out:
        print(1, 2, 3, file=out)


if ismk is not None:
    _write_output()
