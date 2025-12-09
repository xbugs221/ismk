println("Julia script executing!")

@assert ismk.config["test"] == true
@assert ismk.config["foo' bar"] == "let's go"
@assert ismk.params["integer"] == 123
@assert ismk.params["astring"] == "foo\n'\\\" "
@assert ismk.output[1] == "julia.out"
@assert ismk.input[1] == "test.in"
@assert ismk.input["named_input"] == "test.in"

f = open(ismk.output[1], "w")
println(f, "Julia test succeded!")
close(f)
