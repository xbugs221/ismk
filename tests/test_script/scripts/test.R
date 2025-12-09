print(ismk@wildcards)
print(ismk@threads)
print(ismk@log)
print(ismk@config)
print(ismk@params)

if (!is.null(ismk@params[["null_param"]])) {
    stop("Error evaluating null value.")
}
if (ismk@params[["logical_param"]] != TRUE) {
    stop("Error evaluating logical value.")
}
if (ismk@params[["integer_param"]] != 123L || typeof(ismk@params[["integer_param"]]) != "integer") {
    stop("Error evaluating integer.")
}
if (ismk@params[["double_param"]] != 123.0 || typeof(ismk@params[["double_param"]]) != "double") {
    stop("Error evaluating double.")
}
if (!is.nan(ismk@params[["nan_param"]])) {
    stop("Error evaluating NaN.")
}
if (!is.infinite(ismk@params[["inf_param"]]) || ismk@params[["inf_param"]] < 0) {
    stop("Error evaluating infinity.")
}
if (!is.infinite(ismk@params[["neginf_param"]]) || ismk@params[["neginf_param"]] > 0) {
    stop("Error evaluating negative infinity.")
}
if (ismk@params[["complex_param"]] != 1+2i) {
    stop("Error evaluating complex.")
}
if (ismk@params[["character_param"]] != "abc") {
    stop("Error evaluating character.")
}
if (!all.equal(ismk@params[["vector_param"]], c(1, 2, 3))) {
    stop("Error evaluating vector.")
}
if (!identical(ismk@params[["list_param"]], list(TRUE, 123L, "abc"))) {
    stop("Error evaluating list.")
}

if (ismk@config[["test"]] != TRUE) {
    stop("Error evaluating config.")
}

if (ismk@config[["foo\' bar"]] != "let\'s go") {
    stop("Error with the key/value containing single quotes.")
}

values <- scan(ismk@input[[1]])
write(values, file = ismk@output[["txt"]])
