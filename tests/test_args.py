__authors__ = ["K.D. Murray"]
__copyright__ = "Copyright 2024, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"


from ismk.settings.types import Batch


def test_parse_batch():
    from ismk.cli import parse_batch

    assert parse_batch("aggregate=1/2") == Batch("aggregate", 1, 2)
