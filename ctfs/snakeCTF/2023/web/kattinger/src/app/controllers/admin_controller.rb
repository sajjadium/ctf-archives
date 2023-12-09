class AdminController < ApplicationController
  include SessionHelper
  before_action :require_login

  def index
    raise ActionController::RoutingError, 'Unauthorized' unless is_admin?

    @FLAG = ENV['FLAG'] || 'snakeCTF{REDACTED}'
  end
end
