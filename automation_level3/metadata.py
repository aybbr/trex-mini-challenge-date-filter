####
# This script demonstrates how to query the Metadata API using the Tableau
# Server Client.
#
# To run the script, you must have installed Python 2.7.9 or later.
####

import json
import argparse
import getpass
import logging
import requests
import smtplib
from datetime import time

import tableauserverclient as TSC


def main():
    # Set email settings
    gmail_user = ""
    gmail_app_password = ""

    # Set the query https://help.tableau.com/current/api/metadata_api/en-us/docs/meta_api_examples.html
    query = """
    {
       workbooks {
            name 
            owner {
                name
                email
            }
           embeddedDatasources {
               fields {
                   ...on CalculatedField {
                       name
                       }
                }
            }
        }
    }
    """

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
            # Query the Metadata API and store the response in resp
            resp = server.metadata.query(query)
            user_email = resp["data"]["workbooks"][0]["owner"]["email"]
            for wb in resp["data"]["workbooks"]:
                for eds in wb["embeddedDatasources"]:
                    for field in eds["fields"]:
                        if len(field) > 0:
                            s = field.get("name")
                            if s[-1].isdigit():
                                print(s)
                                print(wb.get("name"))
                                print(wb["owner"]["email"])
                                # Build email
                                sent_from = gmail_user
                                sent_to = wb["owner"]["email"]
                                sent_subject = (
                                    "Notification about a data source you published"
                                )
                                sent_body = (
                                    "Hello,\n\n"
                                    "Please review "
                                    + wb.get("name")
                                    + " data source, you have violated the naming conventions for the field: "
                                    + s
                                    + "\n"
                                    "\n"
                                    "Cheers,\n"
                                    "Ayoub\n"
                                )

                                email_text = """\
                                From: %s
                                To: %s
                                Subject: %s
                                
                                %s
                                """ % (
                                    sent_from,
                                    ", ".join(sent_to),
                                    sent_subject,
                                    sent_body,
                                )

                                # Send email
                                try:
                                    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                                    server.ehlo()
                                    server.login(gmail_user, gmail_app_password)
                                    server.sendmail(sent_from, sent_to, email_text)
                                    server.close()

                                    print("Email sent!")
                                except Exception as exception:
                                    print("Error: %s!\n\n" % exception)


if __name__ == "__main__":
    main()
