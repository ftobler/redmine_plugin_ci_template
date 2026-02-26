#!/usr/bin/env python3
"""Bootstrap a fresh Redmine instance for testing."""

import subprocess
import sys

MYSQL = ["docker", "compose", "exec", "-T", "db", "mariadb",
         "-uredmine", "-predmine_password", "redmine"]


def sql(query):
    result = subprocess.run(MYSQL + ["-e", query], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"SQL failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"OK: {query[:60]}...")


# admin user shall no longer change password on first login. it is kept with admin/admin.
sql("UPDATE users SET must_change_passwd = 0 WHERE login = 'admin';")

# enable REST api
sql("INSERT INTO settings (name, value, updated_on) VALUES ('rest_api_enabled', '1', NOW()) ON DUPLICATE KEY UPDATE value = '1';")

# inject a API token to be able to access the database
# userid 1 is the admin, so this has access to everything.
sql("INSERT INTO tokens (user_id, action, value, created_on, updated_on) VALUES (1, 'api', 'testtoken1234', NOW(), NOW());")

# we create a Oauth2 (doorkeeper) Application.
# this is the provider/upstream side
APPLICATION = "OAuthTest"
UID = "sP3or4IOXDMXpNIBwNgz3oEN-IDLXRt_MuhQREsS4Ko"
SECRET = "bB_-2MiwvR5m18gW8Cp-QEO_iMuVtOEMRUG7k0jvzjk"
SECRET_hash = "$2a$12$Giq1rAn8trtzYBJOuWm25OXC1UFq5TQ3zMOfwC7jejR0Ll6XxUMrW"
REDIRECT_URI = "http://localhost:8080/redirect\nhttps://localhost:8081/redirect"  # newline
SCOPES = "view_project search_project view_members"
sql(f"INSERT INTO oauth_applications (id, name, uid, secret, redirect_uri, scopes, confidential, created_at, updated_at) VALUES (1, '{APPLICATION}', '{UID}', '{SECRET_hash}', '{REDIRECT_URI}', '{SCOPES}', 1, NOW(), NOW());")


print("Bootstrap complete.")
