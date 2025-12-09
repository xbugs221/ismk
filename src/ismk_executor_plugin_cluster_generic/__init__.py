from dataclasses import dataclass, field
from typing import Optional

from ismk.executors.local import Executor as LocalExecutor
from ismk.executors.local import common_settings
from ismk.interfaces.executor_plugins.settings import ExecutorSettingsBase


@dataclass
class ExecutorSettings(ExecutorSettingsBase):
    submit_cmd: str = field(
        default="bash",
        metadata={"help": "Command used to submit cluster jobs."},
    )
    status_cmd: Optional[str] = field(
        default=None,
        metadata={"help": "Optional command to query job status."},
    )


Executor = LocalExecutor
