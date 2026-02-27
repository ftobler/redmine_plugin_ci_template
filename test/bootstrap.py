#!/usr/bin/env python3
"""Bootstrap a fresh Redmine instance for testing."""

import subprocess
import sys


APPLICATION = "OAuthTest"
UID = "sP3or4IOXDMXpNIBwNgz3oEN-IDLXRt_MuhQREsS4Ko"
SECRET = "bB_-2MiwvR5m18gW8Cp-QEO_iMuVtOEMRUG7k0jvzjk"
SECRET_HASH = "$2a$12$Giq1rAn8trtzYBJOuWm25OXC1UFq5TQ3zMOfwC7jejR0Ll6XxUMrW"
REDIRECT_URI = "http://localhost:8080/redirect\nhttps://localhost:8081/redirect"  # newline
SCOPES = "view_project search_project view_members"

API_KEY = "testAPIkeyTHROWAWAY123456"

REDMINE_URL_HTTP = "http://localhost"
REDMINE_URL_HTTPS = "https://localhost"


MYSQL = ["docker", "compose", "exec", "-T", "db", "mariadb",
         "-uredmine", "-predmine_password", "redmine"]


def sql(query):
    result = subprocess.run(MYSQL + ["-e", query], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"SQL failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"OK: {query[:60]}...")


def inject_setting(key: str, value: str):
    sql(f"INSERT INTO settings (name, value, updated_on) VALUES ('{key}', '{value}', NOW()) ON DUPLICATE KEY UPDATE value = '{value}';")


def inject_into_db():

    # admin user shall no longer change password on first login. it is kept with admin/admin.
    sql("UPDATE users SET must_change_passwd = 0 WHERE login = 'admin';")

    # enable REST api
    inject_setting("rest_api_enabled", "1")
    inject_setting("protocol", "https")
    inject_setting("host_name", "localhost")
    inject_setting("app_title", "Redmine Throwaway Test Instance")

    # inject a API token to be able to access the database
    # userid 1 is the admin, so this has access to everything.
    sql(f"INSERT INTO tokens (user_id, action, value, created_on, updated_on) VALUES (1, 'api', '{API_KEY}', NOW(), NOW());")

    # we create a Oauth2 (doorkeeper) Application.
    # this is the provider/upstream side
    sql(f"INSERT INTO oauth_applications (id, name, uid, secret, redirect_uri, scopes, confidential, created_at, updated_at) VALUES (1, '{APPLICATION}', '{UID}', '{SECRET_HASH}', '{REDIRECT_URI}', '{SCOPES}', 1, NOW(), NOW());")


    print("Bootstrap complete.")


if __name__ == "__main__":
    inject_into_db()
