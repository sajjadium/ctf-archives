module SessionHelper

    def logged_in?
        !!session[:user_id]
    end
    
    def logout_from_session
        session[:user_id] = nil
    end

    def current_user
        @current_user ||= User.find(session[:user_id]) if !!session[:user_id]
    end

    def is_admin?
        return current_user().username == ENV['ADMIN_USER']
    end
end
