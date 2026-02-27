# Teamplate Project for Redmine Plugin

execute
```
docker compose up
python test/bootstrap.py
```
and it will spin up a throwaway redmine server and initialize it with some defaults. Customize settings in `bootstrap.py`. This allows for running pytests with injected API keys on the CI.