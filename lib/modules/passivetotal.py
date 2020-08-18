#!/usr/bin/env python
##
# omnibus - deadbits.
# passivetotal.com module
##
from requests.auth import HTTPBasicAuth

from ..common import get_apikey
from ..common import warning
from ..http import get


class Plugin(object):

    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['passivetotal'] = None
        self.api_key = get_apikey('passivetotal')
        if self.api_key == '':
            raise TypeError('API keys cannot be left blank | set all keys in etc/apikeys.json')
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    def run(self):
        url = 'https://api.passivetotal.org/v2/dns/passive/unique?query=%s' % self.artifact['name']

        user = self.api_key['user']
        token = self.api_key['key']

        try:
            status, response = get(url, auth=HTTPBasicAuth(user, token))

            if status:
                data = response.json()
                self.artifact['data']['passivetotal'] = data

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
