
infile <- ismk@input[["text_file"]]

# Check the read value is as expected in R.
param_dir <- ismk@params[["param_dir"]]
stopifnot(param_dir == "dir")

outfile <- ismk@output[["out_file"]]
file.create(outfile)
