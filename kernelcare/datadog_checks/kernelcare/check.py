import requests

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.errors import CheckException


class KernelcareCheck(AgentCheck):

    KEY_KCARE_NAGIOS_ENDPOINT = 'https://cln.cloudlinux.com/clweb/api/kcare/nagios/'

    def _parse_nagios_response(self, text):

        lines = text.split('\n')
        _, params = lines[0].split('|', 1)

        res = {}
        for p in params.split(';'):
            k, v = p.split('=', 1)
            res[k] = int(v)
        return res

    def check(self, instance):

        key = instance.get('key')

        if not key:
            raise ConfigurationError('Configuration error, you must provide `key`')

        url = self.KEY_KCARE_NAGIOS_ENDPOINT + key

        response = requests.get(url)
        response.raise_for_status()

        if response.text.startswith('Servers not found for key'):
            raise CheckException(response.text)

        try:
            data = self._parse_nagios_response(response.text)
        except ValueError:
            raise CheckException('Kernelcare API: Invalid Response')

        if 'uptodate' in data:
            self.gauge('kernelcare.uptodate', data['uptodate'])
        if 'outofdate' in data:
            self.gauge('kernelcare.outofdate', data['outofdate'])
        if 'unsupported' in data:
            self.gauge('kernelcare.unsupported', data['unsupported'])
        if 'inactive' in data:
            self.gauge('kernelcare.inactive', data['inactive'])
