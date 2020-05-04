
import json
import argparse
import getpass
import logging
import requests
import tableauserverclient as TSC


def main():
    parser = argparse.ArgumentParser(description="Logs in to the server using PAT.")

    parser.add_argument(
        "--logging-level",
        "-l",
        choices=["debug", "info", "error"],
        default="error",
        help="desired logging level (set to error by default)",
    )

    parser.add_argument("--info", "-i", required=True, help="JSON file with server details",
                        type=argparse.FileType('r'))

    args = parser.parse_args()

    #load json file
    d = json.load(args.info)
    print(d)

    # Set logging level based on user input, or error by default.
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)

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


if __name__ == "__main__":
    main()
