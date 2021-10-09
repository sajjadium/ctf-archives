class ApplicationController < ActionController::Base

    before_action :require_authenticated

    def logged_in?
        session[:user_id].present?
    end

    def require_authenticated
       render status: 401, plain: "Unauthenticated" unless logged_in?
    end
end
