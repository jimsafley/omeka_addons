import requests
from requests.utils import quote

def gh():
    return GitHub()

class GitHub:

    client_id = 'aad23add2728eddf4da3'
    client_secret = '4f44af7870b0dc62bac752d82a1ca52547d360fd'

    def _request(self, endpoint):
        params = {'client_id': self.client_id, 'client_secret': self.client_secret}
        response = requests.get('https://api.github.com' + endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def repo(self, owner, repo):
        endpoint = '/repos/{}/{}'.format(quote(owner), quote(repo))
        return self._request(endpoint)

    def releases(self, owner, repo):
        endpoint = '/repos/{}/{}/releases'.format(quote(owner), quote(repo))
        return self._request(endpoint)
