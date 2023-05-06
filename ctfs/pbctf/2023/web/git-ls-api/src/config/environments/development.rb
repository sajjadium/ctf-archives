require 'active_support/core_ext/integer/time'

Rails.application.configure do
  config.cache_store = :redis_cache_store, { url: 'redis://redis:6379/0', pool_size: 20 }
  config.middleware.use ActionDispatch::Cookies

  config.after_initialize do
    Thread.new do
      loop do
        begin
          Rails.cache.redis.reload { |conn| conn.close }
        rescue
        end
        sleep(5)
      end
    end
  end
end
