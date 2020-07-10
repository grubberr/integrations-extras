from typing import Any

from datadog_checks.base import AgentCheck


class KernelcareCheck(AgentCheck):
    def check(self, _):
        # type: (Any) -> None
        pass
