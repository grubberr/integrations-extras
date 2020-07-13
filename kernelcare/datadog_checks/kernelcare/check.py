import requests

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.errors import CheckException


class KernelcareCheck(AgentCheck):

    KEY_KCARE_NAGIOS_ENDPOINT = 'https://cln.cloudlinux.com/clweb/api/kcare/nagios/'
    RES_KCARE_NAGIOS_ENDPOINT = 'https://cln.cloudlinux.com/clweb/api/kcare/nagios-res/'

    HTTP_RESPONSE_ERRORS = [
        'Servers not found for key',
        'Reseller not found',
        'Registration token not found for reseller',
    ]

    def _parse_nagios_response(self, text):

        lines = text.split('\n')
        tmp = lines[0].split('|', 1)
        if len(tmp) == 1:
            params = tmp[0]
        else:
            params = tmp[1]

        res = {}
        for p in params.split(';'):
            k, v = p.split('=', 1)
            res[k] = int(v)
        return res

    def get_url(self, instance):

        key = instance.get('key')

        if key:
            return self.KEY_KCARE_NAGIOS_ENDPOINT + key

        login = instance.get('login')
        api_token = instance.get('api_token')

        if login and api_token:
            return self.RES_KCARE_NAGIOS_ENDPOINT + login + '/' + api_token

        raise ConfigurationError('Configuration error, you must provide `key` or `login`')

    def check(self, instance):

        url = self.get_url(instance)

        response = requests.get(url)
        response.raise_for_status()

        for prefix in self.HTTP_RESPONSE_ERRORS:
            if response.text.startswith(prefix):
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
