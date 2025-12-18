import textwrap

from ismk.script import ismk


def _write_report():
    with open(ismk.output[0], "w") as f:
        print(
            textwrap.dedent(
                f"""
                <html>
                <head>
                <title>Report</title>
                </head>
                <body>
                    <a href={ismk.report_href("test.html").url_args(foo=4).anchor("bar")}>Link to test.html</a>
                    <a href={ismk.report_href("subdir").child_path("subdir/test3.html")}>Link to subdir/test3.html</a>
                </body>
                </html>
                  """
            ),
            file=f,
        )


if ismk is not None:
    _write_report()
