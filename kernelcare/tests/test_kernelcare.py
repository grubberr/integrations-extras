import pytest

from datadog_checks.base.errors import CheckException
from datadog_checks.kernelcare import KernelcareCheck


@pytest.mark.integration
def test_metric(aggregator, dd_environment, monkeypatch):

    monkeypatch.setattr(KernelcareCheck, 'KEY_KCARE_NAGIOS_ENDPOINT', dd_environment['URL'], raising=True)

    instance = {'key': dd_environment['KEY_FAIL']}
    c = KernelcareCheck('kernelcare', {}, [instance])
    with pytest.raises(CheckException):
        c.check(instance)

    instance = {'key': dd_environment['KEY_OK']}
    c = KernelcareCheck('kernelcare', {}, [instance])
    c.check(instance)

    aggregator.assert_metric('kernelcare.uptodate', value=6, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kernelcare.outofdate', value=3, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kernelcare.unsupported', value=2, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kernelcare.inactive', value=1, metric_type=aggregator.GAUGE)
