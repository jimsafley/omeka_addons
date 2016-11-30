import github3

CLIENT_ID = 'aad23add2728eddf4da3'
CLIENT_SECRET = '4f44af7870b0dc62bac752d82a1ca52547d360fd'

def gh():
    """Get the remote GitHub object."""

    gh = github3.GitHub()
    gh.set_client_id(CLIENT_ID, CLIENT_SECRET)
    return gh
