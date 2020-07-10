from typing import Any, Dict

from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.kernelcare import KernelcareCheck


def test_check(aggregator, instance):
    # type: (AggregatorStub, Dict[str, Any]) -> None
    check = KernelcareCheck('kernelcare', {}, [instance])
    check.check(instance)

    aggregator.assert_all_metrics_covered()
