require_relative 'boot'
require 'securerandom'

require 'active_record/railtie'
# require 'active_storage/engine'
require 'action_controller/railtie'
require 'action_view/railtie'
# require 'action_mailer/railtie'
# require 'active_job/railtie'
require 'action_cable/engine'
# require 'action_mailbox/engine'
require 'action_text/engine'
# require 'rails/test_unit/railtie'
require 'sprockets/railtie'

# Require the gems listed in Gemfile, including any gems
# you've limited to :test, :development, or :production.
Bundler.require(*Rails.groups)

module Kattinger
  class Application < Rails::Application
    # Initialize configuration defaults for originally generated Rails version.
    config.load_defaults 7.0
    config.hosts << ENV['HOST']

    if !ENV.has_key?('SECRET')
      ENV['SECRET'] = SecureRandom.hex(32)
    end

    initializer(:remove_action_mailbox_and_activestorage_routes, after: :add_routing_paths) do |app|
      app.routes_reloader.paths.delete_if { |path| path =~ /activestorage/ }
      app.routes_reloader.paths.delete_if { |path| path =~ /actionmailbox/ }
    end
  end
end
