require 'securerandom'

class ApplicationController < ActionController::Base
  before_action :session

  def session
    Rails.cache.fetch(session_id, expires_in: 5.minutes) do
      { created_at: DateTime.now }
    end.to_json
  end

  def session_id
    @session_id ||= begin
      cookies[:session] = SecureRandom.hex(32) unless cookies[:session]&.match(/\A[0-9a-f]{64}\z/)
      cookies[:session]
    end
  end
end
