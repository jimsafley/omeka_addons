import requests

ROOT_ENDPOINT = 'https://api.github.com'
CLIENT_ID = 'aad23add2728eddf4da3'
CLIENT_SECRET = '4f44af7870b0dc62bac752d82a1ca52547d360fd'

def _request(endpoint):
    params = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
    response = requests.get(ROOT_ENDPOINT + endpoint, params=params)
    response.raise_for_status()
    return response.json()

def repo(owner, repo):
    endpoint = '/repos/{}/{}'.format(requests.utils.quote(owner), requests.utils.quote(repo))
    return _request(endpoint)

def releases(owner, repo):
    endpoint = '/repos/{}/{}/releases'.format(requests.utils.quote(owner), requests.utils.quote(repo))
    return _request(endpoint)
