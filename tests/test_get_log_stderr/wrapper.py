from ismk.shell import shell
shell.executable("bash")
log = ismk.log_fmt_shell(stdout=False, append=True)
shell(
    """
      cat {ismk.input} > {ismk.output}
      (>&2 echo "a stderr message") {log}
      (echo "a stdout message") {log}
      """
)
