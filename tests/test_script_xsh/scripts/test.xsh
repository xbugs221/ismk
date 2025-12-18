echo @($(bcftools --help).splitlines()[1]) > @(ismk.output[0])
