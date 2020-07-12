import pytest
import requests

from datadog_checks.base.errors import CheckException
from datadog_checks.kernelcare import KernelcareCheck


@pytest.mark.integration
def test_metric(aggregator, dd_environment, monkeypatch):

    URL = dd_environment['URL']
    instance_ok = {'key': dd_environment['KEY_OK']}
    instance_fail = {'key': dd_environment['KEY_FAIL']}

    with monkeypatch.context() as m:
        m.setattr(KernelcareCheck, 'KEY_KCARE_NAGIOS_ENDPOINT', URL + '/notfound/', raising=True)
        c = KernelcareCheck('kernelcare', {}, [instance_ok])
        with pytest.raises(requests.HTTPError):
            c.check(instance_ok)

    monkeypatch.setattr(KernelcareCheck, 'KEY_KCARE_NAGIOS_ENDPOINT', URL, raising=True)

    c = KernelcareCheck('kernelcare', {}, [instance_fail])
    with pytest.raises(CheckException):
        c.check(instance_fail)

    c = KernelcareCheck('kernelcare', {}, [instance_ok])
    c.check(instance_ok)

    aggregator.assert_metric('kernelcare.uptodate', value=6, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kernelcare.outofdate', value=3, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kernelcare.unsupported', value=2, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kernelcare.inactive', value=1, metric_type=aggregator.GAUGE)
