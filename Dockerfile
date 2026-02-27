FROM redmine:6.1

# this just demonstrates how to add custom gems in the docker-compose infrastructure.

RUN \
    # echo "gem 'jwt'" >> Gemfile && \
    gosu redmine bundle install && \
    # fix permissions for running as an arbitrary user
	chmod -R ugo=rwX Gemfile.lock "$GEM_HOME" && \
	rm -rf ~redmine/.bundle