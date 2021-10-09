require 'digest'

class LoginController < ApplicationController
  skip_before_action :require_authenticated

  def index
    redirect_to email_url if logged_in?
  end

  def create
    render status: 422, plain: "username is required" unless login_params[:username].present?
    session[:user_id] = Digest::MD5.hexdigest(login_params[:username] + login_params[:password])
    redirect_to email_url
  end

  def login_params
    params.permit(:username, :password)
  end

end
