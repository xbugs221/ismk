from ismk.shell import shell
print("test", file=open(ismk.output[0], "w"))
shell("echo test")