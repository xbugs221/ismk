from ismk import shell
shell.executable("bash")

shell("echo {} > {}".format(ismk.params["title"], ismk.output[0]))
