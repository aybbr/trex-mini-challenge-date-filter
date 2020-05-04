
import json
import requests
import tableauserverclient as TSC

def signin():
    with open('body.json', 'r') as f:
        #load json file
        d = json.load(f)
        print(d)
    # Make sure we use an updated version of the rest apis.
    server = TSC.Server('https://10ax.online.tableau.com/', use_server_version=True)
    # Trying to authenticate using personal access tokens.
    personal_access_token_name = d["credentials"]["personalAccessTokenName"]
    personal_access_token_secret = d["credentials"]["personalAccessTokenSecret"]
    site_name = d["credentials"]["site"]["contentUrl"]
    tableau_auth = TSC.PersonalAccessTokenAuth(
        token_name=personal_access_token_name,
        personal_access_token=personal_access_token_secret,
        site_id=site_name,
    )
    with server.auth.sign_in_with_personal_access_token(tableau_auth):
        print("Logged in successfully")