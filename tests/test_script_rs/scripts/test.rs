use std::io::Write;
println!("Rust script executing!");

assert_eq!(ismk.config.test, true);
assert_eq!(ismk.params.integer, 123);
assert_eq!(ismk.output[0], "rust.out");
assert_eq!(ismk.input[0], "test.in");
assert_eq!(ismk.input.named_input, "test.in");
for (idx, val) in (&ismk.input).into_iter().enumerate() {
    dbg!(idx, &val);
}

let input = &ismk.input;
for value in input {
    dbg!(value);
}

let mut f = std::fs::File::create(&ismk.output[0])?;
write!(&mut f, "Rust test succeded!")?;
