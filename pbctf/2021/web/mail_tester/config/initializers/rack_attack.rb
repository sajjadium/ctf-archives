# frozen_string_literal: true

Rack::Attack.throttle('limit sending emails', limit: 2, period: 30) do |req|
    req.real_ip if req.path == '/email' && req.post?
end