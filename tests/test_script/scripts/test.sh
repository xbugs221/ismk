#!/usr/bin/env bash
set -euo pipefail
exec > "${ismk_output[0]}" 2> "${ismk_log[0]}"
set -x

# Awkward characters are robustly quoted?
test "${ismk_params[astring]}" = $'foo\n\'\\\" ' || echo MISMATCH

echo "The first input file is ${ismk_input[0]}"
echo "The named input file is ${ismk_input[named]}"
echo "The requested number of threads is ${ismk[threads]}"

echo "ismk_config is type ${ismk_config@a}"

echo "The list passed as a parameter is *${ismk_params[alist]}*"
echo "The wildcards are *${ismk_wildcards[bash]}* and *${ismk_wildcards[empty]}*"
echo "The config items are *${ismk_config[test]}* *${ismk_config[testint]}* *${ismk_config[testfloat]}*"
echo "The config item with quotes in is *${ismk_config['foo'"'"' bar']}*"
