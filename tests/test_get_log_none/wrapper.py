from ismk.shell import shell

log = ismk.log_fmt_shell(stdout=False)
shell(
    """
      cat {ismk.input} > {ismk.output}
      (>&2 echo "a stderr message") {log}
      (echo "a stdout message") {log}
      """
)
