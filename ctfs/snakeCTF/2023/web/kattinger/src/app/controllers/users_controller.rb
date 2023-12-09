class UsersController < ApplicationController
  include SessionHelper
  include UsersHelper
  skip_before_action :require_login, only: %i[new create reset reset_submit]

  def user_exists_id?
    return if User.exists?(params[:id])

    raise ActionController::BadRequest, "User doesn't exist"
  end

  def current_user?
    return unless "#{current_user.id}" != params[:id]

    raise ActionController::RoutingError, 'Unauthorized'
  end

  def index
    @users = User.all
  end

  def show
    user_exists_id?

    @account = User.find(params[:id])
  end

  def new
    if logged_in?
      redirect_to root_path
      return
    end
    @account = User.new
  end

  def create
    if logged_in?
      redirect_to root_path
      return
    end

    params[:user][:username] = params[:user][:username].last(8)
    @account = User.new(user_create_params)
    if User.exists?(username: params[:user][:username])
      @message = 'Username already taken!'
      render :new, status: :unprocessable_entity
      return
    end

    if @account.save
      redirect_to :login
      nil
    else
      render :new, status: :unprocessable_entity
    end
  end

  def edit
    user_exists_id?
    current_user?
    # raise ActionController::BadRequest.new("User doesn't exist")

    @account = User.find(params[:id])
  end

  def update
    user_exists_id?
    current_user?
    # raise ActionController::RoutingError.new("User doesn't exist")

    @account = User.find(params[:id])
    if @account.username != ENV['ADMIN_USER']
      if @account.update(user_update_params)
        redirect_to @account
        nil
      else
        @message = 'Error occurred!'
        render :edit, status: :unprocessable_entity
        nil
      end
    else
      @message = 'Please send a certified letter @ Kat Straße, (Meowland) to change the admin password'
      render :edit, status: :unprocessable_entity
      nil
    end
  end

  def reset
    if logged_in?
      redirect_to root_path
      return
    end

    # GET
    if request.get?
      render :reset
      nil
    else
      # POST
      unless User.exists?(username: params[:username].last(8))
        @message = 'User not found!'
        render :reset, status: :unprocessable_entity
        return
      end

      @account = User.find_by(username: params[:username].last(8))
      reset_token = cipher(@account.username)
      @account.update(reset_token: reset_token)
      @account.save
      # TODO: send token by mail
      redirect_to :reset_submit
      nil
    end
  end

  def reset_submit
    if logged_in?
      redirect_to root_path
      return
    end
    @account = User.new

    # GET
    if request.get?
      render :reset_submit
      nil
    else
      # POST
      unless User.exists?(username: params[:user][:username].last(8))
        @message = 'User not found!'
        render :reset_submit, status: :unprocessable_entity
        return
      end

      unless check(params[:user][:username], params[:user][:reset_token])
        @message = 'Wrong reset token!'
        render :reset_submit, status: :unprocessable_entity
        return
      end

      # Not this for now
      # if @account.update(user_reset_params)
      #   @account.update(reset_token: nil)
      #   @account.save
      #   redirect_to :login
      #   return
      # else
      #   @message = "Something went wrong"
      #   render :reset_submit, status: :unprocessable_entity
      # end

      @account = User.find_by(username: params[:user][:username].last(8))
      @message = "Sorry, we're still building the application. Your current password is: " + @account.password
      render :reset_submit, status: :gone
      nil
    end
  end

  def destroy
    user_exists_id?
    current_user?

    @account = User.find(params[:id])
    @account.destroy
    logout_from_session
    redirect_to :login, status: :gone
    nil
  end

  private

  def user_create_params
    params.require(:user).permit(:username, :password, reset_token: nil)
  end

  def user_update_params
    params.require(:user).permit(:password, reset_token: nil)
  end

  def user_reset_params
    params.require(:user).permit(:username, :password, :reset_token)
  end
end
