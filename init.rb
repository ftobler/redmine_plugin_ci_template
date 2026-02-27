

Redmine::Plugin.register :redmine_plugin_ci_template do
  name 'Redmine Plugin Ci Template'
  author 'Florin Tobler'
  author_url 'https://github.com/ftobler'
  description 'Plugin Template. Does nothing.'
  url 'https://github.com/ftobler/redmine_plugin_ci_template'
  version '0.0.1'
  requires_redmine :version_or_higher => '6.1.0'
end