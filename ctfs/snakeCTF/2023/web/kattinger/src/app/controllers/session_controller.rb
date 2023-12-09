class SessionController < ApplicationController
  include SessionHelper
  skip_before_action :require_login

  def new
    @account = User.new
  end

  def home
    if logged_in?
      redirect_to cats_path
    else
      redirect_to login_path
    end
  end

  def login
    return unless logged_in?

    redirect_to root_path
    nil
  end

  def create
    if logged_in?
      redirect_to root_path
      return
    end

    @account = User.find_by(username: params[:username].last(8))
    if !!@account && @account.password === params[:password]
      session[:user_id] = @account.id
      redirect_to root_path
      nil
    else
      @message = 'Wrong username or password'
      render :login, status: :unauthorized
      nil
    end
  end

  def destroy
    logout_from_session
    redirect_to login_path
    nil
  end
end
