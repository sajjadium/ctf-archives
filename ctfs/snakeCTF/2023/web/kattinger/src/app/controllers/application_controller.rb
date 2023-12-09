class ApplicationController < ActionController::Base
  include SessionHelper
  before_action :require_login

  private

  def require_login
    return if logged_in?

    redirect_to login_url
  end
end
