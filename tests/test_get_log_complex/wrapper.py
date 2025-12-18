from ismk.shell import shell
shell.executable("bash")
initial_log = ismk.log_fmt_shell()
stdout_log = ismk.log_fmt_shell(stderr=False, append=True)
stderr_log = ismk.log_fmt_shell(stdout=False, append=True)
shell(
    """
      cat {ismk.input} > {ismk.output}
      echo "should not appear since next line truncates" {initial_log}
      echo "first line" {initial_log}
      (>&2 echo "a stderr message") {stderr_log}
      (echo "a stdout message") {stdout_log}
      """
)
