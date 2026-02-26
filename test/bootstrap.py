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


sql("UPDATE users SET must_change_passwd = 0 WHERE login = 'admin';")
sql("INSERT INTO settings (name, value, updated_on) VALUES ('rest_api_enabled', '1', NOW()) ON DUPLICATE KEY UPDATE value = '1';")
sql("INSERT INTO tokens (user_id, action, value, created_on, updated_on) VALUES (1, 'api', 'testtoken1234', NOW(), NOW());")

print("Bootstrap complete.")
