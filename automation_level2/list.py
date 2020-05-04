import json
import argparse
import getpass
import requests
import tableauserverclient as TSC
from login import signin


def listWorkbook():
    with open("body.json", "r") as f:
        # load json file
        d = json.load(f)
        print(d)
    # Make sure we use an updated version of the rest apis.
    server = TSC.Server("https://10ax.online.tableau.com/", use_server_version=True)
    # Trying to authenticate using personal access tokens.
    personal_access_token_name = d["credentials"]["personalAccessTokenName"]
    personal_access_token_secret = d["credentials"]["personalAccessTokenSecret"]
    site_name = d["credentials"]["site"]["contentUrl"]
    tableau_auth = TSC.PersonalAccessTokenAuth(
        token_name=personal_access_token_name,
        personal_access_token=personal_access_token_secret,
        site_id=site_name,
    )
    with server.auth.sign_in(tableau_auth):
        endpoint = {"workbook": server.workbooks}.get("workbook")
        f = open("creators.csv", "a")
        f.write("workbook,owner\n")
        for resource in TSC.Pager(endpoint.get):
            wb_owner = server.users.get_by_id(resource.owner_id)
            line = resource.name + "," + wb_owner.name + "\n"
            f.write(line)
            print(resource.name, wb_owner.name)
        f.close()
